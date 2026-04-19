from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Bands(BaseModel):
    nir: int | None = None
    red: int | None = None
    red_edge: int | None = None
    blue: int | None = None
    b1: int | None = None
    b2: int | None = None


class ProcessRequest(BaseModel):
    upload_id: str
    algorithm: str

    # фаза роста пшеницы
    growth_stage: Literal["tillering", "booting"]

    # критерий сегментации
    segmentation_level: int = Field(ge=3, le=5)

    # разрешение снимка в сантиметрах на пиксель
    resolution: float = Field(..., gt=0)

    # каналы
    bands: Bands

    @field_validator("resolution", mode="before")
    def parse_resolution(cls, v):
        return float(v.replace(",", ".")) if isinstance(v, str) else v