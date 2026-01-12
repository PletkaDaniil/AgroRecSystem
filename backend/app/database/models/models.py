from datetime import datetime
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Integer,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False,)
    hashed_password: Mapped[str] = mapped_column(String,nullable=False,)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False,)
    is_superuser: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False,)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
