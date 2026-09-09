from fastapi import HTTPException, status

def verify_ownership(upload_id: str, current_user) -> None:
    """
        Проверяем, что upload_id принадлежит текущему пользователю
    """
    if not upload_id.startswith(f"{current_user.id}_"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
