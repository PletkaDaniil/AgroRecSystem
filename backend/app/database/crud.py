from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.database.models.models import User, RefreshToken, Analysis
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


def get_refresh_token_by_token(
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


def get_refresh_token_by_user(
    db: Session,
    user_id: int
) -> RefreshToken | None:
    """
        Получаем refresh-токен по id пользователя
    """
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.user_id == user_id)
        .first()
    )


def update_refresh_token(
    db: Session,
    *,
    refresh_token: RefreshToken,
    token: str,
    expires_at: datetime,
) -> RefreshToken:
    """
        Обновляем refresh токен пользователя
    """
    refresh_token.token = token
    refresh_token.expires_at = expires_at
    refresh_token.created_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(refresh_token)

    return refresh_token


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


# -----------------------------------------------
# Блок функций для анализов: Analysis
# -----------------------------------------------


def create_analysis(
    db: Session,
    *,
    user_id: int,
    upload_id: str,
    algorithm: str,
) -> Analysis:
    """
        Создаем запись о выполненном анализе
    """
    analysis = Analysis(
        user_id=user_id,
        upload_id=upload_id,
        algorithm=algorithm,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def get_latest_analyses_by_user(
    db: Session,
    *,
    user_id: int,
    limit: int = 5,
) -> list[Analysis]:
    """
        Получаем последние 5 анализов пользователя, отсортированные по дате
        Можно занить limit, если нужно будет получить больше или меньше анализов
    """
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .limit(limit)
        .all()
    )


def get_analysis_by_id(
    db: Session,
    analysis_id: int,
) -> Analysis | None:
    """
        Получаем анализ по id
    """
    return (
        db.query(Analysis)
        .filter(Analysis.id == analysis_id)
        .first()
    )
