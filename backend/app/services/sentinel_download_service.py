from pystac_client import Client
import planetary_computer
from shapely.geometry import box
import rasterio
import numpy as np
from rasterio.mask import mask
from rasterio.warp import transform_geom, reproject, Resampling
import requests
import tempfile
import os
from datetime import datetime, timedelta


class SentinelDownloadService:

    def __init__(self):

        # подключение к STAC каталогу Planetary Computer
        self.catalog = Client.open(
            "https://planetarycomputer.microsoft.com/api/stac/v1",
            modifier=planetary_computer.sign_inplace,
        )

    def download_band(self, url, geom):
        
        # временный файл для скачивания band-а
        tmp = tempfile.NamedTemporaryFile(delete=False).name

        # скачивание данных по URL
        with requests.get(url, stream=True) as r:
            r.raise_for_status()

            with open(tmp, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)

        # открываем raster и обрезаем по геометрии
        with rasterio.open(tmp) as src:

            # перевод геометрии в CRS растра
            geom_proj = transform_geom(
                "EPSG:4326",
                src.crs,
                geom.__geo_interface__,
            )

            # маска (обрезка по полигону)
            cropped, transform = mask(src, [geom_proj], crop=True)

            data = cropped[0].astype("float32")

        # удаляем временный файл
        os.remove(tmp)

        return data, transform, src.crs


    def download_tiff(self, bbox, date, out_path):

        # диапазон поиска Sentinel сцен (±14 дней)
        target_date = datetime.fromisoformat(date)
        start_date = target_date - timedelta(days=14)

        # поиск сцен с облачностью < 20%
        search = self.catalog.search(
            collections=["sentinel-2-l2a"],
            bbox=bbox,
            datetime=f"{start_date.date()}/{target_date.date()}",
            query={"eo:cloud_cover": {"lt": 20}},
        )

        items = list(search.items())

        if not items:
            raise RuntimeError("No Sentinel images found")

        # выбираем сцену с минимальной облачностью
        item = min(
            items,
            key=lambda i: i.properties.get("eo:cloud_cover", 100)
        )

        geom = box(*bbox)

        # загрузка основных 10m каналов
        red, transform, crs = self.download_band(item.assets["B04"].href, geom)
        blue, _, _ = self.download_band(item.assets["B02"].href, geom)
        nir, _, _ = self.download_band(item.assets["B08"].href, geom)

        # 20m канал (red edge)
        red_edge_20, transform20, _ = self.download_band(
            item.assets["B05"].href,
            geom
        )

        # приведение 20m -> 10m (upsampling)
        red_edge = np.empty(red.shape, dtype=np.float32)

        reproject(
            source=red_edge_20,
            destination=red_edge,
            src_transform=transform20,
            src_crs=crs,
            dst_transform=transform,
            dst_crs=crs,
            resampling=Resampling.bilinear,
        )

        # формируем финальный stack каналов
        stack = np.stack([red, red_edge, blue, nir])

        # сохраняем GeoTIFF
        with rasterio.open(
            out_path,
            "w",
            driver="GTiff",
            height=stack.shape[1],
            width=stack.shape[2],
            count=4,
            dtype="float32",
            crs=crs,
            transform=transform,
        ) as dst:
            for i in range(4):
                dst.write(stack[i], i + 1)
