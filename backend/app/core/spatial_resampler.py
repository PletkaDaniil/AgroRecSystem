from pathlib import Path
from typing import Union
import shutil
import numpy as np
import rasterio
from scipy.ndimage import gaussian_filter


# целевое пространственное разрешение -> 1 метр на пиксель
TARGET_RESOLUTION_M: float = 1


def resample_to_resolution(
    src_path: Union[str, Path],
    src_resolution_m: float,
    dst_path: Union[str, Path] | None = None,
    target_resolution_m: float = TARGET_RESOLUTION_M,
) -> Path:
    """
        Приводим GeoTIFF к целевому пространственному разрешению
    """
    
    src_path = Path(src_path)

    # формируем путь результата если он не указан
    if dst_path is None:
        dst_path = src_path.with_name(
            f"{src_path.stem}_1m{src_path.suffix}"
        )

    dst_path = Path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)

    # считаем коэффициент изменения разрешения
    block = target_resolution_m // (src_resolution_m / 100.0)

    # если исходное разрешение уже больше метра
    if block <= 1.0:
        shutil.copy2(src_path, dst_path)
        return dst_path

    block_int = int(round(block))

    with rasterio.open(src_path) as src:
        # читаем данные индекса
        data = src.read().astype(np.float32)   # shape: (bands, H, W)

        profile = src.profile.copy()
        transform = src.transform

    bands, H, W = data.shape

    # сглаживаем изображение перед даунсемплингом
    sigma = block / 3.0
    smoothed = gaussian_filter(data, sigma=(0, sigma, sigma))

    # даунсемплируем изображение, усредняя значения внутри блоков размером block x block
    new_H = (H + block_int - 1) // block_int
    new_W = (W + block_int - 1) // block_int

    result = np.full((bands, new_H, new_W), np.nan, dtype=np.float32)

    # усредняем значения внутри каждого блока
    for i in range(new_H):
        for j in range(new_W):

            y0, y1 = i * block_int, min((i + 1) * block_int, H)
            x0, x1 = j * block_int, min((j + 1) * block_int, W)

            tile = smoothed[:, y0:y1, x0:x1]

            # среднее значение индекса внутри блока
            result[:, i, j] = np.nanmean(tile, axis=(1, 2))

    # сохраняем результат в новый TIFF файл
    new_transform = transform * transform.scale(block_int, block_int)
    profile.update(
        height=new_H,
        width=new_W,
        transform=new_transform,
        dtype="float32",
        nodata=np.nan,
        tiled=True,
        blockxsize=256,
        blockysize=256,
        compress="lzw",
    )

    # записываем новый TIFF
    with rasterio.open(dst_path, "w", **profile) as dst:
        dst.write(result)

    return dst_path
