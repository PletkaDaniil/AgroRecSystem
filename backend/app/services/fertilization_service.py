import json
from pathlib import Path
from app.config.fertilization_config import get_fertilization


def generate_fertilization_json(
    result_tif_path: Path,
    algorithm: str,
    growth_stage: str,
    segmentation_level: int,
) -> Path:
    """
        Создаёт JSON файл с рекомендациями на основе конфигурации зон
    """

    # получаем конфигурацию удобрений
    data = get_fertilization(
        algorithm,
        growth_stage,
        segmentation_level,
    )

    json_path = result_tif_path.with_suffix(".json")

    # сохраняем json файл с рекомендациями
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    return json_path
