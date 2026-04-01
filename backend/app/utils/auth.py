from datetime import datetime, timedelta, timezone
from fastapi import Response, HTTPException, status, Cookie, Depends
from sqlalchemy.orm import Session

from app.database.crud import (
    create_refresh_token as db_create_refresh_token,
    get_user_by_id,
)
from app.database.database import get_db
from app.utils.jwt import create_access_token, create_refresh_token, decode_jwt
from app.config.config import settings


def set_cookies(response: Response, access_token: str, refresh_token: str):
    """
        Устанавливаем access и refresh токены в cookies
    """
    response.set_cookie(
        key=settings.auth.access_cookie_name,
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.auth.access_token_expire_seconds,
    )
    response.set_cookie(
        key=settings.auth.refresh_cookie_name,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=settings.auth.refresh_token_expire_seconds,
    )


def decode_refresh(token: str) -> str:
    """
        Декодируем refresh токен и возвращаем jti,
        если токен невалидный — выбрасываем исключение
    """
    try:
        payload = decode_jwt(token)
        jti = payload.get("jti")

        if not jti:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid refresh token",
            )

        return jti

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid refresh token",
        )


def issue_tokens(db: Session, user_id: int) -> tuple[str, str]:
    """
        Создаем новую пару токенов access + refresh
    """
    access_token = create_access_token(user_id)
    refresh_token, jti = create_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=settings.auth.refresh_token_expire_seconds
    )

    db_create_refresh_token(
        db,
        token=jti,
        user_id=user_id,
        expires_at=expires_at,
    )

    return access_token, refresh_token


def get_current_user(
    access_token: str | None = Cookie(
        default=None,
        alias=settings.auth.access_cookie_name
    ),
    db: Session = Depends(get_db)
):
    """
        Получаем текущего пользователя из access-token в cookie
    """

    # проверяем наличие access токена
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token in cookies",
        )

    try:
        # декодируем JWT и извлекаем id пользователя
        payload = decode_jwt(access_token)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token payload",
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid access token",
        )

    # получаем пользователя из БД
    user = get_user_by_id(db, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
        )

    return user
