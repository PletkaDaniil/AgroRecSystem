from pydantic import BaseModel


# Запрос на регистрацию
class RegistrationRequest(BaseModel):
    username: str
    email: str
    password: str


# Запрос на логин
class LoginRequest(BaseModel):
    username: str
    password: str
