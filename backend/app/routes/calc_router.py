from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from pathlib import Path
import hashlib
from app.services.tiff_processing_service import ProcessingService
from app.services.sentinel_download_service import SentinelDownloadService
from app.utils.schemas.calcRequest import CalculatorRequest
from app.utils.schemas.processRequest import Bands
from app.utils.archive import build_result_archive
from app.utils.auth import get_current_user


calculator_router = APIRouter(
    prefix="/calculator",
    tags=["calculator"],
)
TMP_DIR = Path("tmp")
processing_service = ProcessingService()
sentinel_service = SentinelDownloadService()


@calculator_router.post("/")
def process_coords(
    body: CalculatorRequest,
    current_user=Depends(get_current_user),
):
    """
        Обработка поля по координатам через Sentinel-2
    """
    coord_string = f"{body.lat1}{body.lon1}{body.lat2}{body.lon2}"

    # генерируем hash координат
    coord_hash = hashlib.md5(coord_string.encode()).hexdigest()
    upload_id = f"{current_user.id}_{coord_hash}"

    upload_dir = TMP_DIR / upload_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    tif_path = upload_dir / f"{upload_id}.tif"

    try:

        # проверяем существует ли TIFF файл локально
        # если файла нет — скачиваем Sentinel снимок
        if not tif_path.exists():
            sentinel_service.download_tiff(
                bbox=[body.lon1, body.lat1, body.lon2, body.lat2],
                date=body.snap_date,
                out_path=tif_path,
            )

        # настройка каналов Sentinel-2
        bands = Bands(
            nir=4,
            red=1,
            red_edge=2,
            blue=3,
        )

        # запуск обработки TIFF файла
        processing_service.process_tiff(
            tif_path=tif_path,
            algorithm=body.algorithm,
            growth_stage=body.growth_stage,
            segmentation_level=body.segmentation_level,
            resolution=1000,
            bands=bands,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}",
        )

    return {
        "image_url": f"/calculator/image/{upload_id}/{body.algorithm}",
        "archive_url": f"/file/archive/{upload_id}/{body.algorithm}",
        "fert_url": f"/file/fertilization/{upload_id}/{body.algorithm}"
    }


@calculator_router.get("/image/{upload_id}/{algorithm}")
def get_image(upload_id: str):
    """
        Получаем PNG результат сегментации
    """
    path = TMP_DIR / upload_id / f"{upload_id}_result_1m_seg.png"

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="PNG not found",
        )

    return FileResponse(
        path,
        media_type="image/png",
    )


@calculator_router.get("/tif/{upload_id}/{algorithm}")
def get_tif(upload_id: str):
    """
        Получаем TIFF результат сегментации
    """
    path = TMP_DIR / upload_id / f"{upload_id}_result_1m_seg.tif"

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="TIF not found",
        )

    return FileResponse(
        path,
        media_type="image/tiff",
        filename=f"{upload_id}_result.tif",
    )


@calculator_router.get("/fertilization/{upload_id}/{algorithm}")
def get_fertilization(upload_id: str):
    """
        Получаем JSON файл результата количества вносимых удобрений
    """
    path = TMP_DIR / upload_id / f"{upload_id}_result_1m_seg.json"

    if not path.exists():
        raise HTTPException(404, "Fertilization JSON not found")

    return FileResponse(
        path,
        media_type="application/json",
        filename=f"{upload_id}.json",
    )


@calculator_router.get("/archive/{upload_id}/{algorithm}")
def get_archive(upload_id: str):
    upload_dir = TMP_DIR / upload_id
    archive_path = build_result_archive(upload_dir, upload_id)

    return FileResponse(
        archive_path,
        media_type="application/zip",
        filename=f"{upload_id}_result.zip",
    )
