import bcrypt


def hash_password(password: str) -> str:
    """
        Хэшируем пароль перед сохранением в БД
    """
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    ).decode("utf-8")


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
        Проверяем введенный пароль с сохраненным хэшем
    """
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )
