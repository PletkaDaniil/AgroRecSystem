from fastapi import APIRouter, Depends, Response, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.crud import (
    get_user_by_id,
    get_refresh_token_by_token,
    get_user_by_name,
    get_user_by_email,
    create_user
)
from app.utils.password import hash_password, validate_password
from app.utils.auth import set_cookies, decode_refresh, issue_tokens
from app.utils.schemas.user import RegistrationRequest, LoginRequest
from app.config.config import settings
from app.utils.jwt import decode_jwt
from datetime import datetime, timezone


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registration", status_code=status.HTTP_201_CREATED)
def registration(response: Response, data: RegistrationRequest, db: Session = Depends(get_db)) -> dict:
    """
        Регистрация нового пользователя + выдача токенов сразу после регистрации
    """
    # проверяем, что username или email ещё не заняты
    if get_user_by_name(db, data.username) or get_user_by_email(db, data.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    # создаем пользователя 
    hashed_password = hash_password(data.password)
    user = create_user(db, name=data.username, email=data.email, hashed_password=hashed_password)

    # выдаем токены
    access_token, refresh_token = issue_tokens(db, user.id)
    set_cookies(response, access_token, refresh_token)

    return {
        "id": user.id,
        "username": user.name,
        "email": user.email,
        "role": user.role.value,
        "message": "User registered and logged in successfully",
    }


@router.post("/login")
def login(response: Response, data: LoginRequest, db: Session = Depends(get_db)) -> dict:
    """
        Аутентификация пользователя по username или email + выдача токенов
    """
    # ищем пользователя по username
    user = get_user_by_name(db, data.username)

    # если не нашли по username, пробуем найти по email
    if not user:
        user = get_user_by_email(db, data.username)

    # + проверяем пароль
    if not user or not validate_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    # выдаем токены
    access_token, refresh_token = issue_tokens(db, user.id)
    set_cookies(response, access_token, refresh_token)

    return {"message": "Logged in successfully"}


@router.post("/refresh")
def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=settings.auth.refresh_cookie_name),
    db: Session = Depends(get_db)
) -> dict:
    """
        Обновление access и refresh токенов
    """
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")

    #получаем jti и инфу о токене из БД
    jti = decode_refresh(refresh_token)
    token_obj = get_refresh_token_by_token(db, token=jti)

    if not token_obj:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token not found")

    # проверяем истечение срока действия
    if token_obj.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired")

    # + новая пара токенов
    new_access_token, new_refresh_token = issue_tokens(db, token_obj.user_id)
    set_cookies(response, new_access_token, new_refresh_token)

    return {"message": "Tokens refreshed successfully"}


@router.post("/validate")
def validate_user(
    access_token: str | None = Cookie(default=None, alias=settings.auth.access_cookie_name),
    db: Session = Depends(get_db)
) -> dict:
    """
        Проверка валидности access token и получение информации о пользователе
    """
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No access token")

    try:
        # смотрим токен доступа и user_id
        payload = decode_jwt(access_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

    # проверяем, существует ли пользователь
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    return {"user_id": user.id, "role": user.role.value}
