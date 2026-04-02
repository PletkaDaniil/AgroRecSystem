from pydantic import BaseModel, Field
from typing import Literal


class Bands(BaseModel):
    nir: int | None = None
    red: int | None = None
    red_edge: int | None = None
    green: int | None = None
    b1: int | None = None
    b2: int | None = None


class ProcessRequest(BaseModel):
    upload_id: str
    algorithm: str

    # фаза роста пшеницы
    growth_stage: Literal["tillering", "booting"]

    # критерий сегментации
    segmentation_level: int = Field(ge=3, le=5)

    # каналы
    bands: Bands