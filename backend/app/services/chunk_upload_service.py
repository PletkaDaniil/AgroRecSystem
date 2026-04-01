from pathlib import Path
import aiofiles


class UploadService:

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    async def save_chunk(
        self,
        upload_id: str,
        chunk_index: int,
        file,
    ) -> Path:
        """
            Сохраняем chunk загружаемого файла
        """

        upload_dir = self.base_dir / upload_id

        # создаем директорию загрузки
        upload_dir.mkdir(parents=True, exist_ok=True)
        chunk_path = upload_dir / f"chunk_{chunk_index}"

        async with aiofiles.open(chunk_path, "wb") as f:
            # читаем файл блоками по 1MB
            while chunk := await file.read(1024 * 1024):
                await f.write(chunk)

        return chunk_path