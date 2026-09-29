import rasterio
import numpy as np
import planetary_computer
from datetime import datetime, timedelta
from pathlib import Path
from shapely.geometry import box, shape
from pystac_client import Client
from rasterio.mask import mask
from rasterio.warp import transform_geom, reproject, Resampling
from app.utils.exceptions import (
    BadRequestError,
    NotFoundError,
    ExternalServiceError,
)


class SentinelDownloadService:

    STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

    # B02 blue (10m), B04 red (10m), B05 red edge (20m), B08 nir (10m)
    REQUIRED_BANDS = ["B02", "B04", "B05", "B08"]

    def __init__(self, cloud_cover=50, days_back=14):

        # максимальная облачность сцены (%)
        self.cloud_cover = cloud_cover

        # сколько дней назад от целевой даты искать сцены
        self.days_back = days_back

        self.catalog = Client.open(
            self.STAC_URL,
            modifier=planetary_computer.sign_inplace,
        )

    def validate_bbox(self, bbox):
        """
            Проверяем bbox и приводим к формату min_lon, min_lat, max_lon, max_lat
        """
        # порядок углов: min_lon, min_lat, max_lon, max_lat
        lon1, lat1, lon2, lat2 = bbox
        min_lon, max_lon = sorted((lon1, lon2))
        min_lat, max_lat = sorted((lat1, lat2))

        if min_lon == max_lon or min_lat == max_lat:
            raise BadRequestError("Selected area has zero size")

        return [min_lon, min_lat, max_lon, max_lat]

    def find_scene(self, bbox, date):
        """
            Ищем сцену Sentinel-2, которая полностью покрывает bbox и имеет минимальную облачность
        """
        try:
            target_date = datetime.fromisoformat(str(date))
        except ValueError:
            raise BadRequestError("Invalid date format, expected YYYY-MM-DD")

        start_date = target_date - timedelta(days=self.days_back)

        search = self.catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=f"{start_date.date()}/{target_date.date()}",
            query={"eo:cloud_cover": {"lt": self.cloud_cover}},
        )

        items = list(search.items())

        if not items:
            raise NotFoundError("No Sentinel images found for the selected date range")

        # только сцены, которые целиком покрывают область
        geom = box(*bbox)
        covering = [i for i in items if shape(i.geometry).contains(geom)]

        if not covering:
            raise NotFoundError("No single Sentinel scene fully covers the selected area")

        # сцена с минимальной облачностью
        return min(
            covering,
            key=lambda i: i.properties.get("eo:cloud_cover", 100),
        )

    def check_assets(self, item):
        """
            Проверяем, что в сцене есть все необходимые каналы
        """
        for band in self.REQUIRED_BANDS:
            if band not in item.assets:
                raise ExternalServiceError(f"Sentinel scene is missing band {band}")

    def get_band_path(self, item, band_name):
        """
            Получаем URL канала с подписью Azure
        """
        # без подписи Azure не отдает данные
        signed_asset = planetary_computer.sign(item.assets[band_name])
        url = signed_asset.href

        if "sig=" not in url:
            raise ExternalServiceError(f"Failed to sign Sentinel band {band_name} URL")

        # удаленное чтение через GDAL без скачивания файла целиком
        return f"/vsicurl/{url}"

    def read_band(self, item, band_name, geom):
        """
            Читаем канал Sentinel-2 и обрезаем по геометрии
        """
        path = self.get_band_path(item, band_name)

        with rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
            GDAL_HTTP_VERSION="2",
        ):
            with rasterio.open(path) as src:

                # геометрия приводится к CRS растра
                geom_proj = transform_geom(
                    "EPSG:4326",
                    src.crs,
                    geom.__geo_interface__,
                )

                cropped, transform = mask(src, [geom_proj], crop=True)

                return {
                    "data": cropped[0].astype("float32"),
                    "transform": transform,
                    "crs": src.crs,
                    "resolution": src.res,
                }

    def resample_to_reference(self, band, reference):
        """
            Ресэмплируем канал к эталонной сетке
        """
        # 20m -> 10m на сетку эталонного канала
        resampled = np.empty(reference["data"].shape, dtype=np.float32)

        reproject(
            source=band["data"],
            destination=resampled,
            src_transform=band["transform"],
            src_crs=band["crs"],
            dst_transform=reference["transform"],
            dst_crs=reference["crs"],
            resampling=Resampling.bilinear,
        )

        return resampled

    def check_alignment(self, reference, *bands):
        """
            Проверяем, что все каналы выровнены
        """
        for band in bands:

            if band["data"].shape != reference["data"].shape:
                raise ExternalServiceError("Sentinel bands have different shapes")

            if band["transform"] != reference["transform"]:
                raise ExternalServiceError("Sentinel bands are not aligned")

    def save_tiff(self, stack, reference, out_path):
        """
            Сохраняем многоканальный TIFF файл
        """
        # 0 считается отсутствием данных (вне полигона и на краях)
        with rasterio.open(
            out_path,
            "w",
            driver="GTiff",
            height=stack.shape[1],
            width=stack.shape[2],
            count=stack.shape[0],
            dtype="float32",
            crs=reference["crs"],
            transform=reference["transform"],
            nodata=0,
        ) as dst:
            for i in range(stack.shape[0]):
                dst.write(stack[i], i + 1)

    def download_tiff(self, bbox, date, out_path):
        """
            Загружаем многоканальный TIFF файл с данными Sentinel-2
        """
        out_path = Path(out_path)

        bbox = self.validate_bbox(bbox)

        item = self.find_scene(bbox, date)
        self.check_assets(item)

        geom = box(*bbox)

        # blue задает эталонную сетку
        blue = self.read_band(item, "B02", geom)
        red = self.read_band(item, "B04", geom)
        nir = self.read_band(item, "B08", geom)
        red_edge_20 = self.read_band(item, "B05", geom)

        self.check_alignment(blue, red, nir)

        red_edge = self.resample_to_reference(red_edge_20, blue)

        # порядок каналов: red, red_edge, blue, nir
        stack = np.stack([red["data"], red_edge, blue["data"], nir["data"]])

        # запись через временный файл, чтобы при сбое не остался битый tif
        tmp_path = out_path.with_name(out_path.name + ".part")
        try:
            self.save_tiff(stack, blue, tmp_path)
            tmp_path.replace(out_path)
        finally:
            tmp_path.unlink(missing_ok=True)

        # фактическая дата съемки может отличаться от запрошенной
        return item.datetime
