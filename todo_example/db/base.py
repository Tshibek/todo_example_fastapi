import uuid
from datetime import datetime

from sqlalchemy import UUID, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from todo_example.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )
