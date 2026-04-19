import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    vmin:  float
    vmax:  float
    color: str


# ─────────────────────────────────────────────────────────────────────────────
# КОНФИГУРАЦИЯ РЕЕСТРА ЗОН СЕГМЕНТАЦИИ
# ─────────────────────────────────────────────────────────────────────────────

ZONE_REGISTRY: dict[tuple[str, str, int], list[Zone]] = {

    # ── ChlRI | кущение ──────────────────────────────────────────────────────

    ("ChlRI", "tillering", 5): [
        Zone(-np.inf, 0.39, "#C0392B"),
        Zone( 0.39,   0.41, "#E67E22"),
        Zone( 0.41,   0.43, "#F1C40F"),
        Zone( 0.43,   0.45, "#A8D08D"),
        Zone( 0.45, +np.inf, "#27AE60"),
    ],

    ("ChlRI", "tillering", 4): [
        Zone(-np.inf, 0.39, "#C0392B"),
        Zone( 0.39,   0.42, "#E67E22"),
        Zone( 0.42,   0.45, "#F1C40F"),
        Zone( 0.45, +np.inf, "#27AE60"),
    ],

    ("ChlRI", "tillering", 3): [
        Zone(-np.inf, 0.39, "#C0392B"),
        Zone( 0.39,   0.45, "#F1C40F"),
        Zone( 0.45, +np.inf, "#27AE60"),
    ],

    # ── ChlRI | выход в трубку ───────────────────────────────────────────────

    ("ChlRI", "booting", 5): [
        Zone(-np.inf, 0.41, "#C0392B"),
        Zone( 0.41,   0.44, "#E67E22"),
        Zone( 0.44,   0.47, "#F1C40F"),
        Zone( 0.47,   0.51, "#A8D08D"),
        Zone( 0.51, +np.inf, "#27AE60"),
    ],

    ("ChlRI", "booting", 4): [
        Zone(-np.inf, 0.41, "#C0392B"),
        Zone( 0.41,   0.45, "#E67E22"),
        Zone( 0.45,   0.51, "#F1C40F"),
        Zone( 0.51, +np.inf, "#27AE60"),
    ],

    ("ChlRI", "booting", 3): [
        Zone(-np.inf, 0.41, "#C0392B"),
        Zone( 0.41,   0.51, "#F1C40F"),
        Zone( 0.51, +np.inf, "#27AE60"),
    ],

    # ── RPImod | кущение ─────────────────────────────────────────────────────

    # ("RPImod", "tillering", 5): [
    #     Zone(-np.inf, 0.38, "#C0392B"),
    #     Zone( 0.38,   0.42, "#E67E22"),
    #     Zone( 0.42,   0.46, "#F1C40F"),
    #     Zone( 0.46,   0.50, "#A8D08D"),
    #     Zone( 0.50, +np.inf, "#27AE60"),
    # ],

    # ── RPImod | выход в трубку ──────────────────────────────────────────────

    # ("RPImod", "booting", 5): [
    #     Zone(-np.inf, 0.35, "#C0392B"),
    #     Zone( 0.35,   0.39, "#E67E22"),
    #     Zone( 0.39,   0.43, "#F1C40F"),
    #     Zone( 0.43,   0.47, "#A8D08D"),
    #     Zone( 0.47, +np.inf, "#27AE60"),
    # ],

    # ── NDVI | кущение ───────────────────────────────────────────────────────

    # ("NDVI", "tillering", 5): [
    #     Zone(-np.inf, 0.30, "#C0392B"),
    #     Zone( 0.30,   0.45, "#E67E22"),
    #     Zone( 0.45,   0.60, "#F1C40F"),
    #     Zone( 0.60,   0.75, "#A8D08D"),
    #     Zone( 0.75, +np.inf, "#27AE60"),
    # ],

    # ── NDVI | выход в трубку ────────────────────────────────────────────────

    ("NDVI", "booting", 5): [
        Zone(-np.inf, 0.45, "#C0392B"),
        Zone( 0.45,   0.60, "#E67E22"),
        Zone( 0.60,   0.72, "#F1C40F"),
        Zone( 0.72,   0.82, "#A8D08D"),
        Zone( 0.82, +np.inf, "#27AE60"),
    ],

    ("NDVI", "booting", 5): [
        Zone(-np.inf, 0.45, "#C0392B"),
        Zone( 0.45,   0.64, "#E67E22"),
        Zone( 0.64,   0.82, "#F1C40F"),
        Zone( 0.82, +np.inf, "#27AE60"),
    ],

    ("NDVI", "booting", 3): [
        Zone(-np.inf, 0.45, "#C0392B"),
        Zone( 0.45,   0.82, "#F1C40F"),
        Zone( 0.82, +np.inf, "#27AE60"),
    ],
}


def get_zones(algorithm: str, growth_stage: str, segmentation_level: int) -> list[Zone]:
    """
        Получаем набор зон сегментации для визуализации индекса
    """

    # формируем ключ доступа к реестру зон
    key = (algorithm, growth_stage, segmentation_level)

    # проверяем наличие конфигурации
    if key not in ZONE_REGISTRY:
        raise ValueError(
            f"Комбинация {key} не найдена в реестре зон."
        )

    return ZONE_REGISTRY[key]