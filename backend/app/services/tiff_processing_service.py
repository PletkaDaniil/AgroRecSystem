from pathlib import Path
from app.core.geo_index import IndexProcessor, NDVI, ChlRI, RPImod
from app.core.spatial_resampler import resample_to_resolution
from app.core.segmentation import segment_tiff
from app.utils.schemas.processRequest import Bands
from app.services.fertilization_service import generate_fertilization_json
from app.utils.shapefile import tif_to_shapefile


class ProcessingService:
    """
        Сервис обработки гиперспектральных TIFF изображений
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
        growth_stage: str,
        segmentation_level: int,
        resolution: float,
        bands: Bands,
    ) -> tuple[Path, Path, Path]:
        """
            Обрабатываем TIFF и возвращаем пути к результатам
        """

        if algorithm not in self.algorithms:
            raise ValueError(f"Unknown algorithm: {algorithm}")
 
        band_map: dict[str, int] = bands.model_dump()
        index_class = self.algorithms[algorithm]

        # задаем для RPImod параметр c1 (нам нужен именно 0.5)
        index = (
            index_class(band_map=band_map, c1=0.5)
            if algorithm == "RPImod"
            else index_class(band_map=band_map)
        )

        processor = IndexProcessor()
        result_tif = processor.process(
            src_path=tif_path,
            index=index,
        )
 
        # ресемплинг
        resampled_tif = resample_to_resolution(
            src_path=result_tif,
            src_resolution_m=resolution,
        )

        # сегментация
        result_tif, result_png = segment_tiff(
            src_path=resampled_tif,
            algorithm=algorithm,
            growth_stage=growth_stage,
            segmentation_level=segmentation_level,
        )

        generate_fertilization_json(
            result_tif_path=result_tif,
            algorithm=algorithm,
            growth_stage=growth_stage,
            segmentation_level=segmentation_level,
        )

        base = str(result_tif).removesuffix(".tif")
        shp_path = f"{base}.shp"

        tif_to_shapefile(
            tif_path=str(result_tif),
            shp_path=shp_path,
            nodata_class=None,
        )

        return result_tif, result_png, shp_path
