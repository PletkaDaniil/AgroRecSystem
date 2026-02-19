from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# определяем корневую папку
BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWTSettings(BaseSettings):
    """
        Настраиваем JWT-аутентификацию (ключи, алгоритм, время жизни токенов, cookie)
    """
    private_key: Path = Field(default=BASE_DIR / "keys" / "jwt-private.pem")
    public_key: Path = Field(default=BASE_DIR / "keys" / "jwt-public.pem")
    algorithm: str = "RS256"

    # время жизни access-токена (в секундах)
    access_token_expire_seconds: int = 10
    # время жизни refresh-токена (в секундах)
    refresh_token_expire_seconds: int = 30

    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"


class CORSSettings(BaseSettings):
    """
        Настраиваем CORS (параметры доступа)
    """
    allow_origins: list[str] = Field(default=[
        "http://localhost:5173"
    ])
    # разрешаем передачу cookie
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class DatabaseSettings(BaseSettings):
    """
        Настраиваем параметры подключения к БД
    """
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    PG_DBNAME: str

    # загружаем настройки из файла .env
    model_config = SettingsConfigDict(env_file=".env")


class Settings(BaseSettings):
    """
        Общие настройки приложения
    """
    auth: AuthJWTSettings = AuthJWTSettings()
    cors: CORSSettings = CORSSettings()
    db = DatabaseSettings()


settings = Settings()
