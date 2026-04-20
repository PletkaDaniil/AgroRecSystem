from pathlib import Path
from typing import Union
import shutil
import numpy as np
import rasterio
from rasterio.enums import Resampling


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
    block = target_resolution_m / (src_resolution_m / 100.0)

    # если исходное разрешение уже больше целевого
    if block <= 1.0:
        shutil.copy2(src_path, dst_path)
        return dst_path

    block_int = int(round(block))

    with rasterio.open(src_path) as src:
        H, W = src.height, src.width

        # вычисляем размеры результирующего растра
        new_H = (H + block_int - 1) // block_int
        new_W = (W + block_int - 1) // block_int

        profile = src.profile.copy()
        profile.update(
            height=new_H,
            width=new_W,
            transform=src.transform * src.transform.scale(block_int, block_int),
            dtype="float32",
            nodata=np.nan,
            tiled=True,
            blockxsize=256,
            blockysize=256,
            compress="lzw",
        )

        # усредняем блоки
        with rasterio.open(dst_path, "w", **profile) as dst:
            for band_idx in range(1, src.count + 1):
                data = src.read(
                    band_idx,
                    out_shape=(new_H, new_W),
                    resampling=Resampling.average,
                ).astype(np.float32)

                # записываем новый TIFF
                dst.write(data, band_idx)

    return dst_path
