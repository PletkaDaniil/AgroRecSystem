import uuid
import jwt
from datetime import datetime, timedelta, timezone
from app.config.config import settings


# читаем ключи для подписи и проверки JWT-токенов
PRIVATE_KEY = settings.auth.private_key.read_text()
PUBLIC_KEY = settings.auth.public_key.read_text()


def encode_jwt(
    payload: dict,
    *,
    expire_delta: timedelta,
) -> str:
    """
        Создаем JWT-токен
    """
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)

    # добавляем в токен время создания (iat) и время истечения (exp)
    to_encode.update(
        exp=now + expire_delta,
        iat=now,
    )

    return jwt.encode(
        to_encode,
        PRIVATE_KEY,
        algorithm=settings.auth.algorithm,
    )


def decode_jwt(token: str | bytes) -> dict:
    """
        Декодируем JWT-токен
    """
    return jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=[settings.auth.algorithm],
    )


def create_access_token(user_id: int) -> str:
    """
        Создаем access-токен для пользователя
    """
    return encode_jwt(
        payload={
            "sub": str(user_id),
            "type": "access",
        },
        expire_delta=timedelta(
            seconds=settings.auth.access_token_expire_seconds
        ),
    )


def create_refresh_token() -> tuple[str, str]:
    """
        Создаем refresh-токен и его уникальный идентификатор (jti)
    """
    jti = uuid.uuid4().hex

    token = encode_jwt(
        payload={
            "jti": jti,
            "type": "refresh",
        },
        expire_delta=timedelta(
            seconds=settings.auth.refresh_token_expire_seconds
        ),
    )

    return token, jti
