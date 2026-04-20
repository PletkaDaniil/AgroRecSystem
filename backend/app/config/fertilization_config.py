FERTILIZATION_REGISTRY: dict[tuple[str, str, int], dict[int, dict]] = {

    # ── ChlRI | кущение ───────────────────────────────────────────────

    ("ChlRI", "tillering", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("ChlRI", "tillering", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("ChlRI", "tillering", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },

    # ── ChlRI | выход в трубку ────────────────────────────────────────

    ("ChlRI", "booting", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("ChlRI", "booting", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("ChlRI", "booting", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },

    # ── RPImod | кущение ───────────────────────────────────────────────

    ("RPImod", "tillering", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("RPImod", "tillering", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("RPImod", "tillering", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },

    # ── RPImod | выход в трубку ────────────────────────────────────────

    ("RPImod", "booting", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("RPImod", "booting", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("RPImod", "booting", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },

    # ── NDVI | кущение ───────────────────────────────────────────────

    ("NDVI", "tillering", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("NDVI", "tillering", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("NDVI", "tillering", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },

    # ── NDVI | выход в трубку ────────────────────────────────────────

    ("NDVI", "booting", 5): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 90},
        2: {"color": "#F1C40F", "value": 60},
        3: {"color": "#A8D08D", "value": 30},
        4: {"color": "#27AE60", "value": 0},
    },

    ("NDVI", "booting", 4): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#E67E22", "value": 80},
        2: {"color": "#F1C40F", "value": 40},
        3: {"color": "#27AE60", "value": 0},
    },

    ("NDVI", "booting", 3): {
        0: {"color": "#C0392B", "value": 120},
        1: {"color": "#F1C40F", "value": 60},
        2: {"color": "#27AE60", "value": 0},
    },
}

def get_fertilization(
    algorithm: str,
    growth_stage: str,
    segmentation_level: int,
) -> dict[int, dict]:

    key = (algorithm, growth_stage, segmentation_level)

    if key not in FERTILIZATION_REGISTRY:
        raise ValueError(
            f"Комбинация {key} не найдена в реестре зон."
        )

    return FERTILIZATION_REGISTRY[key]
