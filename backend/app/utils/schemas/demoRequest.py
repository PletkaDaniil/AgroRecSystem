from pydantic import BaseModel, Field

# Запрос на запуск демонстрационного анализа
class DemoRunRequest(BaseModel):
    demo_id: str
    segmentation_level: int = Field(ge=3, le=5)
