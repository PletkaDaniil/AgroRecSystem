import zipfile
from pathlib import Path
from fastapi import HTTPException

# Указываем, какие файлы включаем в архив и под каким именем отдаем
ARCHIVE_MEMBERS = {
    "png": ("result.png", "_result_1m_seg.png"),
    "tif": ("result.tif", "_result_1m_seg.tif"),
    "shp": ("result.shp", "_result_1m_seg.shp"),
    "shx": ("result.shx", "_result_1m_seg.shx"),
    "dbf": ("result.dbf", "_result_1m_seg.dbf"),
    "prj": ("result.prj", "_result_1m_seg.prj"),
    "cpg": ("result.cpg", "_result_1m_seg.cpg"),
}

def build_result_archive(upload_dir: Path, upload_id: str) -> Path:
    """
        Собираем zip-архив со всеми результатами обработки
    """
    archive_path = upload_dir / f"{upload_id}_result.zip"

    found_any = False
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for _, (arcname, suffix) in ARCHIVE_MEMBERS.items():
            src = upload_dir / f"{upload_id}{suffix}"
            if src.exists():
                zf.write(src, arcname=arcname)
                found_any = True

    if not found_any:
        archive_path.unlink(missing_ok=True)
        raise HTTPException(status_code=404, detail="Result files not found")

    return archive_path