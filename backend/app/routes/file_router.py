from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from fastapi.responses import FileResponse
from pathlib import Path
from app.services.chunk_upload_service import UploadService
from app.services.tiff_processing_service import ProcessingService
from app.utils.chunk_merge import merge_chunks
from app.utils.schemas.uploadRequest import CreateUploadRequest
from app.utils.auth import get_current_user


file_router = APIRouter(
    prefix="/file",
    tags=["file"],
)
TMP_DIR = Path("tmp")
upload_service = UploadService(TMP_DIR)
processing_service = ProcessingService()


@file_router.post("/create-upload")
def create_upload(
    body: CreateUploadRequest,
    current_user=Depends(get_current_user),
):
    """
        Создаем новую загрузку файла
    """

    upload_id = f"{current_user.id}_{body.file_hash}_{body.algorithm}"
    upload_dir = TMP_DIR / upload_id

    # проверяем был ли файл уже обработан
    already_processed = (
        any(upload_dir.glob("*_result.tif"))
        if upload_dir.exists()
        else False
    )

    return {
        "upload_id": upload_id,
        "already_processed": already_processed,
    }



@file_router.post("/upload-chunk")
async def upload_chunk(
    upload_id: str,
    chunk_index: int,
    file: UploadFile,
):
    """
        Загружаем chunk файла
    """
    try:
        await upload_service.save_chunk(
            upload_id,
            chunk_index,
            file,
        )
        return {"status": "ok"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save chunk: {str(e)}",
        )



@file_router.get("/upload-status/{upload_id}")
def get_status(upload_id: str):
    """
        Получаем список загруженных чанков
    """
    upload_dir = TMP_DIR / upload_id

    if not upload_dir.exists():
        return []

    chunk_files = list(upload_dir.glob("chunk_*"))

    uploaded_indices = sorted(
        int(p.name.split("_")[1])
        for p in chunk_files
    )

    return uploaded_indices


@file_router.post("/upload-complete")
def complete_upload(
    upload_id: str,
    total_chunks: int,
):
    """
        Завершаем загрузку и объединяем чанки
    """
    upload_dir = TMP_DIR / upload_id
    if not upload_dir.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Upload directory not found",
        )

    try:
        final_file = merge_chunks(
            upload_id,
            total_chunks,
            TMP_DIR,
        )
        for chunk_file in upload_dir.glob("chunk_*"):
            chunk_file.unlink()

        return {
            "file_path": str(final_file),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to merge chunks: {str(e)}",
        )


@file_router.post("/process")
def process_file(
    upload_id: str,
    algorithm: str,
):
    """
        Запускаем обработку TIFF файла
    """
    upload_dir = TMP_DIR / upload_id
    tif_path = upload_dir / f"{upload_id}.tif"

    if not tif_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TIF file not found",
        )
    try:
        processing_service.process_tiff(
            tif_path=tif_path,
            algorithm=algorithm,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {str(e)}",
        )

    return {
        "image_url": f"/file/image/{upload_id}/{algorithm}",
        "tif_url": f"/file/tif/{upload_id}/{algorithm}",
    }


@file_router.get("/image/{upload_id}/{algorithm}")
def get_image(upload_id: str):
    """
        Получаем PNG изображение результата
    """
    path = TMP_DIR / upload_id / f"{upload_id}_result.png"

    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PNG not found",
        )

    return FileResponse(
        path,
        media_type="image/png",
    )


@file_router.get("/tif/{upload_id}/{algorithm}")
def get_tif(upload_id: str):
    """
        Получаем TIFF файл результата
    """
    path = TMP_DIR / upload_id / f"{upload_id}_result.tif"

    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="TIF not found",
        )

    return FileResponse(
        path,
        media_type="image/tiff",
        filename=f"{upload_id}_result.tif",
    )