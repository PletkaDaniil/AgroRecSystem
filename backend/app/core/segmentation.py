from pathlib import Path
from typing import Union
import numpy as np
import rasterio
from rasterio.windows import Window
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter, binary_opening, binary_closing
from app.config.zones_config import get_zones


# размер тайла для обработки больших TIFF
TILE_SIZE = 1024

# уровень сглаживания сегментации
SMOOTH = 1


def segment_tile(tile: np.ndarray, zones) -> np.ndarray:
    """
        Преобразовываем значение индекса в классы зон

        Каждый пиксель получает: номер зоны (class_id)
    """

    out = np.full(tile.shape, -1, dtype=np.int8)

    for z in zones:

        # проверяем попадание в диапазон зоны
        lo = tile >= z.vmin if np.isfinite(z.vmin) else np.ones_like(tile, bool)
        hi = tile <  z.vmax if np.isfinite(z.vmax) else np.ones_like(tile, bool)

        mask = lo & hi & ~np.isnan(tile)

        # присваиваем класс зоны (явный class_id)
        out[mask] = z.class_id

    return out


def smooth(zone_map: np.ndarray, zones) -> np.ndarray:
    """
        Убираем шум в сегментации через медианный фильтр + морфологию
    """

    # если сглаживание выключено
    if SMOOTH <= 1:
        return zone_map

    # медианный фильтр (убирает шум)
    sm = median_filter(zone_map, size=SMOOTH)

    canvas = sm.copy()

    # морфологическая очистка по каждому классу
    class_ids = [z.class_id for z in zones]

    for cid in class_ids:

        mask = sm == cid

        if mask.any():
            opened = binary_opening(mask, iterations=1)
            closed = binary_closing(opened, iterations=1)

            canvas[closed] = cid

    return canvas


def segment_tiff(
    src_path: Union[str, Path],
    algorithm: str,
    growth_stage: str,
    segmentation_level: int,
    dst_tif: Union[str, Path] | None = None,
    dst_png: Union[str, Path] | None = None,
):
    """
        1. считываем индекс
        2. разбиваем на тайлы
        3. классифицируем по зонам
        4. сглаживаем результат
        5. сохраняем GeoTIFF + PNG результата
    """

    src_path = Path(src_path)

    # получаем зоны сегментации
    zones = get_zones(algorithm, growth_stage, segmentation_level)

    # формируем пути результата
    if dst_tif is None:
        dst_tif = src_path.with_name(f"{src_path.stem}_seg.tif")

    if dst_png is None:
        dst_png = src_path.with_name(f"{src_path.stem}_seg.png")

    dst_tif = Path(dst_tif)
    dst_png = Path(dst_png)

    with rasterio.open(src_path) as src:

        H, W = src.height, src.width
        meta = src.profile.copy()
        nodata = src.nodata

        meta.update(
            dtype="int8",
            count=1,
            nodata=-1,
            compress="lzw"
        )

        with rasterio.open(dst_tif, "w", **meta) as dst:

            # проходим по тайлам изображения
            for r0 in range(0, H, TILE_SIZE):
                for c0 in range(0, W, TILE_SIZE):

                    r1 = min(r0 + TILE_SIZE, H)
                    c1 = min(c0 + TILE_SIZE, W)

                    win = Window(c0, r0, c1 - c0, r1 - r0)

                    # читаем индекс
                    tile = src.read(1, window=win).astype(np.float32)

                    # заменяем NoData на NaN
                    if nodata is not None:
                        tile[tile == nodata] = np.nan

                    # сегментация
                    seg = segment_tile(tile, zones)

                    # сглаживание
                    seg = smooth(seg, zones)

                    # запись результата
                    dst.write(seg, 1, window=win)

    with rasterio.open(dst_tif) as src:
        preview = src.read(1)

    # cтроим корректное RGB-изображение, опираясь на class_id
    class_to_rgb = {}
    for z in zones:
        r = int(z.color[1:3], 16)
        g = int(z.color[3:5], 16)
        b = int(z.color[5:7], 16)
        class_to_rgb[z.class_id] = (r, g, b)

    H, W = preview.shape
    rgb = np.zeros((H, W, 3), dtype=np.uint8)

    for class_id, (r, g, b) in class_to_rgb.items():
        mask = preview == class_id
        rgb[mask] = (r, g, b)

    plt.figure(figsize=(10, 10))
    plt.imshow(rgb)
    plt.axis("off")

    dst_png.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(dst_png, bbox_inches="tight", pad_inches=0)
    plt.close()

    return dst_tif, dst_png