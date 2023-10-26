import datetime
from typing import TypeVar

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from todo_example.db.base import Base

ModelType = TypeVar("ModelType")


class UserModel(Base):
    """Model for demo purpose."""

    __tablename__ = "users_model"

    username: Mapped[str] = mapped_column(
        String(length=200),
        unique=True,
    )  # noqa: WPS432
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    login_attempts: Mapped[int] = mapped_column(Integer(), default=0)
    locked_until: Mapped[datetime.datetime] = mapped_column(nullable=True)

    def __str__(self) -> str:
        return self.username
