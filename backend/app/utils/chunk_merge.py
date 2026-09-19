from pathlib import Path
import shutil


def merge_chunks(
    upload_id: str,
    total_chunks: int,
    base_dir: Path,
) -> Path:
    """
        Объединяем чанки файла в итоговый файл
    """

    upload_dir = base_dir / upload_id

    # путь к итоговому tif файлу
    final_path = upload_dir / f"{upload_id}.tif"

    tmp_path = upload_dir / f"{upload_id}.tif.merging"
    try:
        with open(tmp_path, "wb") as final:

            # последовательно читаем каждый chunk
            for index in range(total_chunks):
                chunk_path = upload_dir / f"chunk_{index}"

                # читаем файл блоками по 1MB
                with open(chunk_path, "rb") as chunk:
                    shutil.copyfileobj(chunk, final, 8 * 1024 * 1024)

        # теперь .tif появляется только целиком
        tmp_path.replace(final_path)

    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise

    return final_path
