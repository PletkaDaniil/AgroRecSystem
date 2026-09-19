from app.utils.exceptions import ForbiddenError

def verify_ownership(upload_id: str, current_user) -> None:
    """
        Проверяем, что upload_id принадлежит текущему пользователю
    """
    if not upload_id.startswith(f"{current_user.id}_"):
        raise ForbiddenError("Access denied")
