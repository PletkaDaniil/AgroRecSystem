from pathlib import Path


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

    with open(final_path, "wb") as final:

        # последовательно читаем каждый chunk
        for index in range(total_chunks):

            chunk_path = upload_dir / f"chunk_{index}"

            with open(chunk_path, "rb") as chunk:

                # читаем файл блоками по 1MB
                while data := chunk.read(1024 * 1024):
                    final.write(data)

    return final_path