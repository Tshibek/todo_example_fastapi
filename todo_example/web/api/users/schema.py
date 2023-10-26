import datetime
import re
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    password2: str

    class Config:
        from_attributes = True

    @field_validator("password")
    def validate_password(cls, value):
        # Walidacja hasła
        if len(value) < 8:
            raise ValueError("Hasło musi mieć co najmniej 8 znaków.")
        if not re.search(r"\d", value):
            raise ValueError("Hasło musi zawierać przynajmniej jedną cyfrę (0-9).")
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Hasło musi zawierać przynajmniej jedną wielką literę (A-Z).",
            )
        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Hasło musi zawierać przynajmniej jedną małą literę (a-z).",
            )
        if not re.search(r"[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", value):
            raise ValueError("Hasło musi zawierać przynajmniej jeden znak specjalny.")

        return value

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegister":
        pw1 = self.password
        pw2 = self.password2
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError("Hasła nie są takie same")
        return self


class UserDetailSchema(BaseModel):
    id: uuid.UUID
    username: str
    password: str
    email: str
    locked_until: Optional[datetime.datetime] = None
    login_attempts: Optional[int]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
