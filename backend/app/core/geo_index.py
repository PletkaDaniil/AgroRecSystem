from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Union

import numpy as np
import rasterio
from rasterio.windows import Window


WINDOW_SIZE = 1024


# ─────────────────────────────────────────────────────────────────────────────
# ЧТЕНИЕ GEOTIFF
# ─────────────────────────────────────────────────────────────────────────────

class GeoTiffReader:
    """
        Чтение GeoTIFF файла с поддержкой тайловой обработки
    """

    def __init__(self, dataset: rasterio.io.DatasetReader):
        self._ds = dataset

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "GeoTiffReader":
        """
            Открываем GeoTIFF файл
        """
        path = Path(path)

        # проверяем существование файла
        if not path.exists():
            raise FileNotFoundError(path)

        return cls(rasterio.open(path))

    @property
    def width(self) -> int:
        # ширина изображения
        return self._ds.width

    @property
    def height(self) -> int:
        # высота изображения
        return self._ds.height

    @property
    def crs(self):
        # система координат
        return self._ds.crs

    @property
    def transform(self):
        # affine transform (геопривязка)
        return self._ds.transform

    def read_bands(self, bands: list[int], window: Window | None = None) -> dict[int, np.ndarray]:
        """
            Читаем нужные каналы изображения
        """
        # читаем только нужные bands
        return {b: self._ds.read(b, window=window).astype(np.float32) for b in bands}

    def iter_windows(self) -> Generator[Window, None, None]:
        """
            Итерация по изображению окнами размера WINDOW_SIZE (сейчас 1024x1024)
        """
        for row in range(0, self.height, WINDOW_SIZE):
            for col in range(0, self.width, WINDOW_SIZE):

                window = Window(
                    col,
                    row,
                    min(WINDOW_SIZE, self.width - col),
                    min(WINDOW_SIZE, self.height - row)
                )

                yield window

    def __enter__(self) -> "GeoTiffReader":
        return self

    def __exit__(self, *_) -> None:
        # закрываем dataset
        self._ds.close()


# ─────────────────────────────────────────────────────────────────────────────
# ЗАПИСЬ GEOTIFF
# ─────────────────────────────────────────────────────────────────────────────

class GeoTiffWriter:
    """
        Запись GeoTIFF файла с тайловой структурой
    """

    def __init__(self, dataset: rasterio.io.DatasetWriter):
        self._ds = dataset

    @classmethod
    def create(cls, path: Union[str, Path], width: int, height: int, crs, transform) -> "GeoTiffWriter":
        """
            Создаем новый GeoTIFF файл для записи
        """
        path = Path(path)

        # создаем директорию если её нет
        path.parent.mkdir(parents=True, exist_ok=True)

        ds = rasterio.open(
            path,
            mode="w",
            driver="GTiff",
            width=width,
            height=height,
            count=1,  # один канал (индекс)
            crs=crs,
            transform=transform,
            dtype="float32",
            nodata=np.nan,
            tiled=True,       # включаем тайлы
            blockxsize=256,   # размер тайла
            blockysize=256,
            compress="lzw",   # сжатие
        )

        return cls(ds)

    def write_window(self, data: np.ndarray, window: Window) -> None:
        """
            Записываем результат для одного тайла
        """
        # rasterio ожидает форму (bands, height, width)
        self._ds.write(data[np.newaxis, :, :], window=window)

    def __enter__(self) -> "GeoTiffWriter":
        return self

    def __exit__(self, *_) -> None:
        # закрываем файл
        self._ds.close()


# ─────────────────────────────────────────────────────────────────────────────
# СПЕКТРАЛЬНЫЕ ИНДЕКСЫ
# ─────────────────────────────────────────────────────────────────────────────

class SpectralIndex(ABC):
    """
        Базовый класс спектрального индекса
    """

    def __init__(self, band_map: dict[str, int]):
        # соответствие роли канала -> номер канала
        self._band_map = band_map

        # определяем какие каналы нужны для индекса
        self.required_bands = self._resolve_required_bands()

    def _resolve_required_bands(self) -> list[int]:
        # преобразуем роли каналов в реальные band numbers
        return [self._band_map[role] for role in self._required_roles]

    @property
    @abstractmethod
    def _required_roles(self) -> list[str]:
        """
            Какие каналы нужны для вычисления индекса
        """
        ...

    @abstractmethod
    def compute(self, bands: dict[int, np.ndarray]) -> np.ndarray:
        """
            Вычисление индекса
        """
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__


class NDVI(SpectralIndex):
    # NDVI = (NIR - Red) / (NIR + Red)

    @property
    def _required_roles(self) -> list[str]:
        return ["nir", "red"]

    def compute(self, bands: dict[int, np.ndarray]) -> np.ndarray:
        nir = bands[self._band_map["nir"]]
        red = bands[self._band_map["red"]]

        # добавляем epsilon чтобы избежать деления на 0
        return (nir - red) / (nir + red + 1e-6)


class ChlRI(SpectralIndex):
    # Chlorophyll Reflectance Index
    # (NIR - RedEdge) / (NIR + RedEdge - 2 * Blue)

    @property
    def _required_roles(self) -> list[str]:
        return ["nir", "red_edge", "blue"]

    def compute(self, bands: dict[int, np.ndarray]) -> np.ndarray:
        nir      = bands[self._band_map["nir"]]
        red_edge = bands[self._band_map["red_edge"]]
        blue     = bands[self._band_map["blue"]]

        return (nir - red_edge) / (nir + red_edge - 2 * blue + 1e-6)


class RPImod(SpectralIndex):
    # Modified Redness Pigment Index
    # c1 - ((B1 - B2) / (B1 + B2))

    def __init__(self, band_map: dict[str, int], c1: float = 0.5):
        self.c1 = c1
        super().__init__(band_map)

    @property
    def _required_roles(self) -> list[str]:
        return ["b1", "b2"]

    def compute(self, bands: dict[int, np.ndarray]) -> np.ndarray:
        b1 = bands[self._band_map["b1"]]
        b2 = bands[self._band_map["b2"]]

        return self.c1 - ((b1 - b2) / (b1 + b2 + 1e-6))


# ─────────────────────────────────────────────────────────────────────────────
# ОБРАБОТКА TIFF И ВЫЧИСЛЕНИЕ ИНДЕКСОВ
# ─────────────────────────────────────────────────────────────────────────────

class IndexProcessor:
    """
        Основной процессор вычисления спектральных индексов
    """

    def process(
        self,
        src_path: Union[str, Path],
        index: SpectralIndex,
        dst_path: Union[str, Path] | None = None,
    ) -> tuple[Path, str]:

        src_path = Path(src_path)

        # если путь результата не указан — создаем рядом с исходным файлом
        if dst_path is None:
            dst_path = src_path.with_name(f"{src_path.stem}_result.tif")
        else:
            dst_path = Path(dst_path)

        with GeoTiffReader.from_file(src_path) as reader:

            with GeoTiffWriter.create(
                path=dst_path,
                width=reader.width,
                height=reader.height,
                crs=reader.crs,
                transform=reader.transform,
            ) as writer:

                # проходим по тайлам изображения
                for window in reader.iter_windows():

                    # читаем нужные каналы
                    raw = reader.read_bands(index.required_bands, window)

                    # вычисляем индекс
                    result = index.compute(raw)

                    # записываем результат
                    writer.write_window(result, window)

        return dst_path