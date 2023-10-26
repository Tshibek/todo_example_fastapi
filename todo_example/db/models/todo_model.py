import uuid
from enum import Enum as PyEnum
from typing import TypeVar

from sqlalchemy import UUID, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from todo_example.db.base import Base

ModelType = TypeVar("ModelType")


class StatusEnum(PyEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TodoModel(Base):
    __tablename__ = "todo_model"
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users_model.id"),
    )
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text())
    status: Mapped[StatusEnum] = mapped_column(
        Enum(StatusEnum),
        default=StatusEnum.TODO,
    )
