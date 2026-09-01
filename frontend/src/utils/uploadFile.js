import api from '@/api/http'

const CHUNK_SIZE = 20 * 1024 * 1024 // 20 MB
const SAMPLE_SIZE = 2 * 1024 * 1024 // 2 MB на сэмпл

function readSlice(file, start, end) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload  = () => resolve(new Uint8Array(reader.result))
    reader.onerror = () => reject(reader.error)
    reader.readAsArrayBuffer(file.slice(start, end))
  })
}

async function hashFile(file) {
  let buffer

  // Для небольших файлов хэшируем полностью
  if (file.size <= SAMPLE_SIZE * 3) {
    buffer = await readSlice(file, 0, file.size)
  } else {

    // Для больших файлов берем начало, середину и конец
    // + добавляем размер файла для снижения коллизий
    const mid    = Math.floor(file.size / 2)
    const start  = await readSlice(file, 0, SAMPLE_SIZE)
    const center = await readSlice(file, mid - SAMPLE_SIZE / 2, mid + SAMPLE_SIZE / 2)
    const end    = await readSlice(file, file.size - SAMPLE_SIZE, file.size)

    const sizeBytes = new Uint8Array(8)
    new DataView(sizeBytes.buffer).setBigUint64(0, BigInt(file.size), false)

    const merged = new Uint8Array(start.length + center.length + end.length + 8)
    let offset = 0
    for (const chunk of [start, center, end, sizeBytes]) {
      merged.set(chunk, offset)
      offset += chunk.length
    }

    buffer = merged
  }

  const hashBuffer = await crypto.subtle.digest('SHA-256', buffer)

  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
    .slice(0, 32)
}

function splitChunks(file, chunkSize = CHUNK_SIZE) {
  const chunks = []
  let offset = 0

  // Разбиваем файл на чанки фиксированного размера
  while (offset < file.size) {
    chunks.push(file.slice(offset, offset + chunkSize))
    offset += chunkSize
  }

  return chunks
}

export async function uploadFile(
  file,
  formula,
  processPayload,
  { onProgress, onStage } = {}
) {
  const notify   = (stage) => onStage?.(stage)
  const progress = (pct)   => onProgress?.(Math.round(pct))

  // 1. Хэшируем файл
  notify('hashing')
  progress(0)

  const fileHash = await hashFile(file)

  // 2. Создаем upload сессию
  const { data: { upload_id: uploadId, file_ready } } =
    await api.post('/file/create-upload', {
      file_hash:  fileHash,
      algorithm:  formula,
      resolution: processPayload.resolution,
    })

  // 3. Загружаем чанки если tif еще не готов
  if (!file_ready) {
    const chunks = splitChunks(file)
    const total  = chunks.length

    notify('resume')

    const { data: uploaded } = await api.get(`/file/upload-status/${uploadId}`)
    const done = new Set(uploaded)

    notify('uploading')

    for (let i = 0; i < total; i++) {

      if (done.has(i)) {
        progress(5 + ((i + 1) / total) * 75)
        continue
      }

      const fd = new FormData()
      fd.append('file', chunks[i], file.name)

      try {
        await api.post('/file/upload-chunk', fd, {
          params: { upload_id: uploadId, chunk_index: i },
        })
      } catch (error) {
        throw error
      }

      progress(5 + ((i + 1) / total) * 75)
    }

    notify('merging')
    progress(82)

    try {
      await api.post('/file/upload-complete', null, {
        params: { upload_id: uploadId, total_chunks: total },
      })
    } catch (error) {
      throw error
    }

    progress(88)

  } else {
    // tif уже существует — пропускаем загрузку
    progress(88)
  }

  // 4. Обработка файла
  notify('processing')

  try {
    const { data } = await api.post('/file/process', {
      upload_id: uploadId,
      ...processPayload,
    })

    progress(100)
    notify('done')

    return {
      imageUrl:   data.image_url,
      archiveUrl: data.archive_url,
      fertUrl:    data.fert_url,
      uploadId,
    }

  } catch (error) {
    throw error
  }
}