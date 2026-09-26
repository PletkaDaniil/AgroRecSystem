import os
import shutil
import threading
from pathlib import Path
from app.services.tiff_processing_service import ProcessingService
from app.utils.schemas.processRequest import Bands
from app.utils.exceptions import NotFoundError, BadRequestError

DEMO_DIR = Path("demo")
DEMO_SRC = DEMO_DIR / "sources"
DEMO_CACHE = DEMO_DIR / "cache"
SEG_LEVELS = (3, 4, 5)

# Описание демо примера
DEMOS: dict[str, dict] = {
    "demo-1": {
        "title": "Пример 1",
        "description": "Гиперспектральная-съёмка, фаза «выход в трубку»",
        "source": "demo.tiff",
        "date": "2024-06-11",
        "algorithm": "ChlRI",
        "growth_stage": "booting",
        "resolution": 5.0,
        "bands": {"nir": 175, "red_edge": 152, "blue": 29},
    },
    "demo-2": {
        "title": "Пример 2",
        "description": "Гиперспектральная-съёмка, фаза «выход в трубку»",
        "source": "demo.tiff",
        "date": "2024-06-11",
        "algorithm": "NDVI",
        "growth_stage": "booting",
        "resolution": 5.0,
        "bands": {"nir": 175, "red": 140},
    },
    "demo-3": {
        "title": "Пример 3",
        "description": "Гиперспектральная-съёмка, фаза «выход в трубку»",
        "source": "demo.tiff",
        "date": "2024-06-11",
        "algorithm": "PRImod",
        "growth_stage": "booting",
        "resolution": 5.0,
        "bands": {"b1": 88, "b2": 70},
    },
}


class DemoService:
    def __init__(self):
        self._processing = ProcessingService()
        self._locks: dict[str, threading.Lock] = {}
        self._guard = threading.Lock()

    def _lock_for(self, key: str) -> threading.Lock:
        with self._guard:
            return self._locks.setdefault(key, threading.Lock())

    def get_demo(self, demo_id: str) -> dict:
        demo = DEMOS.get(demo_id)
        if demo is None:
            raise NotFoundError("Demo project not found")
        return demo

    @staticmethod
    def key(demo_id: str, level: int) -> str:
        return f"demo_{demo_id}_s{level}"

    def ensure_result(self, demo_id: str, level: int) -> tuple[str, Path]:
        """
            Возвращаем (upload_id-подобный ключ, папка с результатами)
            Если результата ещё нет — считаем и кэшируем
        """
        demo = self.get_demo(demo_id)
        if level not in SEG_LEVELS:
            raise BadRequestError("segmentation_level must be 3, 4 or 5")

        key = self.key(demo_id, level)
        out_dir = DEMO_CACHE / key

        # маркер вне папки, чтобы не попал в архив
        done = DEMO_CACHE / f"{key}.done"

        if done.exists():
            return key, out_dir

        with self._lock_for(key):
            # пока ждали лок, уже посчитали
            if done.exists():
                return key, out_dir

            src = DEMO_SRC / demo["source"]
            if not src.exists():
                raise NotFoundError("Demo source file is missing on server")

            shutil.rmtree(out_dir, ignore_errors=True)
            out_dir.mkdir(parents=True)
            tif = out_dir / f"{key}.tif"
            try:
                # без копирования гигабайтов
                os.link(src, tif)
            except OSError:
                shutil.copy(src, tif)

            try:
                self._processing.process_tiff(
                    tif_path=tif,
                    algorithm=demo["algorithm"],
                    growth_stage=demo["growth_stage"],
                    segmentation_level=level,
                    resolution=demo["resolution"],
                    bands=Bands(**demo["bands"]),
                )
            except ValueError as e:
                shutil.rmtree(out_dir, ignore_errors=True)
                raise BadRequestError(str(e))
            except Exception:
                shutil.rmtree(out_dir, ignore_errors=True)
                raise

            done.touch()
        return key, out_dir


demo_service = DemoService()
