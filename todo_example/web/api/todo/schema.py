import uuid

from pydantic import BaseModel


class TodoSchema(BaseModel):
    id: uuid.UUID
    title: str
    description: str

    class Config:
        from_attributes = True


class TodoCreateSchema(BaseModel):
    title: str
    description: str
