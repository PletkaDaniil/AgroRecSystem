from fastapi import APIRouter, Depends
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.database.crud import get_latest_analyses_by_user
from app.utils.auth import get_current_user

users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/me")
def get_me(user = Depends(get_current_user)) -> dict:
    return {
        "id": user.id,
        "username": user.name,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat() if getattr(user, "created_at", None) else None,
    }


@users_router.get("/me/analyses/latest")
def get_my_latest_analyses(
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict]:
    analyses = get_latest_analyses_by_user(db, user_id=user.id, limit=5)

    return [
        {
            "id": a.id,
            "upload_id": a.upload_id,
            "algorithm": a.algorithm,
            "created_at": a.created_at.isoformat(),
            "archive_url": f"/file/archive/{a.upload_id}/{a.algorithm}",
        }
        for a in analyses
    ]
