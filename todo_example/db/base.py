from sqlalchemy.orm import DeclarativeBase

from todo_example.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
