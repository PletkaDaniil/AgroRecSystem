import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    vmin: float
    vmax: float
    color: str
    class_id: int


# ─────────────────────────────────────────────────────────────────────────────
# КОНФИГУРАЦИЯ РЕЕСТРА ЗОН СЕГМЕНТАЦИИ
# ─────────────────────────────────────────────────────────────────────────────

ZONE_REGISTRY: dict[tuple[str, str, int], list[Zone]] = {

    # ── ChlRI | кущение ──────────────────────────────────────────────────────

    ("ChlRI", "tillering", 5): [
        Zone(-np.inf, 0.39, "#C0392B", 0),
        Zone( 0.39,   0.41, "#E67E22", 1),
        Zone( 0.41,   0.43, "#F1C40F", 2),
        Zone( 0.43,   0.45, "#A8D08D", 3),
        Zone( 0.45, +np.inf, "#27AE60", 4),
    ],

    ("ChlRI", "tillering", 4): [
        Zone(-np.inf, 0.39, "#C0392B", 0),
        Zone( 0.39,   0.42, "#E67E22", 1),
        Zone( 0.42,   0.45, "#F1C40F", 2),
        Zone( 0.45, +np.inf, "#27AE60", 3),
    ],

    ("ChlRI", "tillering", 3): [
        Zone(-np.inf, 0.39, "#C0392B", 0),
        Zone( 0.39,   0.45, "#F1C40F", 1),
        Zone( 0.45, +np.inf, "#27AE60", 2),
    ],

    # ── ChlRI | выход в трубку ───────────────────────────────────────────────

    ("ChlRI", "booting", 5): [
        Zone(-np.inf, 0.41, "#C0392B", 0),
        Zone( 0.41,   0.44, "#E67E22", 1),
        Zone( 0.44,   0.47, "#F1C40F", 2),
        Zone( 0.47,   0.51, "#A8D08D", 3),
        Zone( 0.51, +np.inf, "#27AE60", 4),
    ],

    ("ChlRI", "booting", 4): [
        Zone(-np.inf, 0.41, "#C0392B", 0),
        Zone( 0.41,   0.45, "#E67E22", 1),
        Zone( 0.45,   0.51, "#F1C40F", 2),
        Zone( 0.51, +np.inf, "#27AE60", 3),
    ],

    ("ChlRI", "booting", 3): [
        Zone(-np.inf, 0.41, "#C0392B", 0),
        Zone( 0.41,   0.51, "#F1C40F", 1),
        Zone( 0.51, +np.inf, "#27AE60", 2),
    ],

    # ── RPImod | кущение ─────────────────────────────────────────────────────

    ("RPImod", "tillering", 5): [
        Zone(-np.inf, 0.46925, "#C0392B", 0),
        Zone( 0.46925,   0.4745, "#E67E22", 1),
        Zone( 0.4745,   0.47975, "#F1C40F", 2),
        Zone( 0.47975,   0.485, "#A8D08D", 3),
        Zone( 0.485, +np.inf, "#27AE60", 4),
    ],

    ("RPImod", "tillering", 4): [
        Zone(-np.inf, 0.46925, "#C0392B", 0),
        Zone( 0.46925,   0.477125, "#E67E22", 1),
        Zone( 0.477125,   0.485, "#F1C40F", 2),
        Zone( 0.485, +np.inf, "#27AE60", 3),
    ],

    ("RPImod", "tillering", 3): [
        Zone(-np.inf, 0.46925, "#C0392B", 0),
        Zone( 0.46925,   0.485, "#F1C40F", 1),
        Zone( 0.485, +np.inf, "#27AE60", 2),
    ],

    # ── RPImod | выход в трубку ──────────────────────────────────────────────

    ("RPImod", "booting", 5): [
        Zone(-np.inf, 0.47925, "#C0392B", 0),
        Zone( 0.47925,   0.4845, "#E67E22", 1),
        Zone( 0.4845,   0.48975, "#F1C40F", 2),
        Zone( 0.48975,   0.495, "#A8D08D", 3),
        Zone( 0.495, +np.inf, "#27AE60", 4),
    ],

    ("RPImod", "booting", 4): [
        Zone(-np.inf, 0.47925, "#C0392B", 0),
        Zone( 0.47925,   0.487125, "#E67E22", 1),
        Zone( 0.487125,   0.495, "#F1C40F", 2),
        Zone( 0.495, +np.inf, "#27AE60", 3),
    ],

    ("RPImod", "booting", 3): [
        Zone(-np.inf, 0.47925, "#C0392B", 0),
        Zone( 0.47925,   0.495, "#F1C40F", 1),
        Zone( 0.495, +np.inf, "#27AE60", 2),
    ],

    # ── NDVI | кущение ───────────────────────────────────────────────────────

    ("NDVI", "tillering", 5): [
        Zone(-np.inf, 0.4, "#C0392B", 0),
        Zone( 0.4,   0.55, "#E67E22", 1),
        Zone( 0.55,  0.67, "#F1C40F", 2),
        Zone( 0.67,  0.77, "#A8D08D", 3),
        Zone( 0.77, +np.inf, "#27AE60", 4),
    ],

    ("NDVI", "tillering", 4): [
        Zone(-np.inf, 0.4, "#C0392B", 0),
        Zone( 0.4,   0.59, "#E67E22", 1),
        Zone( 0.59,  0.77, "#F1C40F", 2),
        Zone( 0.77, +np.inf, "#27AE60", 3),
    ],

    ("NDVI", "tillering", 3): [
        Zone(-np.inf, 0.4, "#C0392B", 0),
        Zone( 0.4,   0.77, "#F1C40F", 1),
        Zone( 0.77, +np.inf, "#27AE60", 2),
    ],

    # ── NDVI | выход в трубку ────────────────────────────────────────────────

    ("NDVI", "booting", 5): [
        Zone(-np.inf, 0.45, "#C0392B", 0),
        Zone( 0.45,   0.60, "#E67E22", 1),
        Zone( 0.60,   0.72, "#F1C40F", 2),
        Zone( 0.72,   0.82, "#A8D08D", 3),
        Zone( 0.82, +np.inf, "#27AE60", 4),
    ],

    ("NDVI", "booting", 4): [
        Zone(-np.inf, 0.45, "#C0392B", 0),
        Zone( 0.45,   0.64, "#E67E22", 1),
        Zone( 0.64,   0.82, "#F1C40F", 2),
        Zone( 0.82, +np.inf, "#27AE60", 3),
    ],

    ("NDVI", "booting", 3): [
        Zone(-np.inf, 0.45, "#C0392B", 0),
        Zone( 0.45,   0.82, "#F1C40F", 1),
        Zone( 0.82, +np.inf, "#27AE60", 2),
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

    return sorted(ZONE_REGISTRY[key], key=lambda z: z.class_id)