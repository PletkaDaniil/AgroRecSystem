from pathlib import Path
from app.core.geo_index import (
    IndexProcessor,
    IndexVisualizer,
    ChlRI,
    NDVI,
    RPImod,
)


class ProcessingService:
    """
        Сервис обработки 300-канальных TIFF изображений
    """

    def __init__(self):
        # алгоритмы расчета индексов
        self.algorithms = {
            "ChlRI": ChlRI,
            "NDVI": NDVI,
            "RPImod": RPImod,
        }

    def process_tiff(
        self,
        tif_path: Path,
        algorithm: str,
    ) -> tuple[Path, Path]:
        """
            Обрабатываем TIFF и возвращаем пути к результатам
        """

        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        index_class = self.algorithms[algorithm]

        # задаем для RPImod параметр c1 (нам нужен именно 0.5)
        index = index_class() if algorithm != "RPImod" else index_class(c1=0.5)

        processor = IndexProcessor()

        # формируем пути для результатов
        result_tif = tif_path.with_name(f"{tif_path.stem}_result.tif")
        result_png = tif_path.with_name(f"{tif_path.stem}_result.png")

        # вычисляем индекс
        processor.process(
            src_path=tif_path,
            index=index,
            dst_path=result_tif,
        )

        # и сохраняем визуализацию
        IndexVisualizer().save(result_tif, result_png)

        return result_tif, result_png