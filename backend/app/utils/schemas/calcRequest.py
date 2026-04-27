from pydantic import BaseModel
from typing import Literal

class CalculatorRequest(BaseModel):
    
    lat1: float
    lon1: float
    lat2: float
    lon2: float

    snap_date: str

    algorithm: str

    growth_stage: Literal["tillering", "booting"]

    segmentation_level: int