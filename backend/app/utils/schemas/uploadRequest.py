from pydantic import BaseModel

# Запрос на загрузку файла для обработки
class CreateUploadRequest(BaseModel):
    file_hash: str
    algorithm: str
