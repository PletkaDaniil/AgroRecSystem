from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.demo_service import demo_service
from app.utils.schemas.demoRequest import DemoRunRequest
from app.utils.archive import build_result_archive
from app.utils.exceptions import NotFoundError

demo_router = APIRouter(prefix="/demo", tags=["demo"])


@demo_router.get("/list")
def list_demos():
    """
        Список демо-проектов
    """
    return demo_service.list_public()


@demo_router.get("/preview/{demo_id}")
def get_preview(demo_id: str):
    return FileResponse(demo_service.preview_path(demo_id))


@demo_router.post("/run")
def run_demo(body: DemoRunRequest):
    """
        Выдаем результат - формат как у /file/process
    """
    demo_service.ensure_result(body.demo_id, body.segmentation_level)
    base = f"{body.demo_id}/{body.segmentation_level}"
    return {
        "image_url": f"/demo/image/{base}",
        "archive_url": f"/demo/archive/{base}",
        "fert_url": f"/demo/fertilization/{base}",
    }


@demo_router.get("/image/{demo_id}/{level}")
def demo_image(demo_id: str, level: int):
    key, d = demo_service.ensure_result(demo_id, level)
    path = d / f"{key}_result_1m_seg.png"
    if not path.exists():
        raise NotFoundError("PNG not found")
    return FileResponse(path, media_type="image/png")


@demo_router.get("/fertilization/{demo_id}/{level}")
def demo_fertilization(demo_id: str, level: int):
    key, d = demo_service.ensure_result(demo_id, level)
    path = d / f"{key}_result_1m_seg.json"
    if not path.exists():
        raise NotFoundError("Fertilization JSON not found")
    return FileResponse(path, media_type="application/json", filename=f"{key}.json")


@demo_router.get("/archive/{demo_id}/{level}")
def demo_archive(demo_id: str, level: int):
    key, d = demo_service.ensure_result(demo_id, level)
    try:
        archive_path = build_result_archive(d, key)
    except FileNotFoundError as e:
        raise NotFoundError(f"Result files not found: {e}")
    return FileResponse(archive_path, media_type="application/zip", filename=f"{key}_result.zip")
