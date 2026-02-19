from datetime import datetime
from sqlalchemy.orm import Session
from app.database.models.models import User, RefreshToken
from app.database.models.roles import UserRole


# -----------------------------------------------
# Блок функций для пользователя: User
# -----------------------------------------------


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
        Получаем пользователя по id
    """
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_name(db: Session, name: str) -> User | None:
    """
        Получаем пользователя по логину (name)
    """
    return (
        db.query(User)
        .filter(User.name == name)
        .first()
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    """
        Получаем пользователя по email
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def create_user(
    db: Session,
    *,
    name: str,
    email: str,
    hashed_password: str,
    role: UserRole = UserRole.user,
) -> User:
    """
        Создаем нового пользователя
    """
    user = User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    *,
    user: User,
) -> None:
    """
        Удаляем пользователя
    """
    db.delete(user)
    db.commit()


'''
def update_user_role(
    db: Session,
    *,
    user: User,
    role: UserRole,
) -> User:
    """
        Обновляем роль пользователя
    """
    user.role = role
    db.commit()
    db.refresh(user)
    return user
'''


# -----------------------------------------------
# Блок функций для refresh-токенов: RefreshToken
# -----------------------------------------------


def create_refresh_token(
    db: Session,
    *,
    token: str,
    user_id: int,
    expires_at: datetime,
) -> RefreshToken:
    """
        Создаем refresh-токен
    """
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def get_refresh_token(
    db: Session,
    token: str,
) -> RefreshToken | None:
    """
        Получаем refresh-токен по значению токена
    """
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token)
        .first()
    )


def delete_refresh_token(
    db: Session,
    *,
    refresh_token: RefreshToken,
) -> None:
    """
        Удаляем конкретный refresh-токен
    """
    db.delete(refresh_token)
    db.commit()


def delete_user_refresh_tokens(
    db: Session,
    *,
    user_id: int,
) -> None:
    """
        Удаляем все refresh-токены пользователя (например при logout со всех устройств)
    """
    (
        db.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()
