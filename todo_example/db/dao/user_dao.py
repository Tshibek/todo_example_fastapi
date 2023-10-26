import datetime

from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError

from todo_example.db.dao.base_dao import BaseDAO
from todo_example.db.models.user_model import UserModel
from todo_example.services.authentication.hash_password import (
    hash_password,
    verify_password,
)
from todo_example.services.authentication.security import TokenAuthentication
from todo_example.settings import settings
from todo_example.utils.enums.exceptions import AuthException
from todo_example.web.api.users.schema import UserDetailSchema, UserRegister


class UserDAO(BaseDAO):
    async def register_user(self, user_input: UserRegister):
        try:
            user_data = user_input.model_dump(exclude={"password2"})
            hashed_password = hash_password(user_data["password"])
            user = UserModel(
                password=hashed_password,
                username=user_data["username"],
                email=user_data["email"],
            )
            self.session.add(user)
            await self.session.commit()
            return {"message": "User registered successfully"}
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthException.USER_ALREADY_EXIST,
            )

    async def get_user_by_username(self, object_name: str) -> UserDetailSchema:
        return await self.get_object_by_name(
            UserModel,
            "username",
            object_name,
            UserDetailSchema,
        )

    async def login(self, response: Response, form_data: OAuth2PasswordRequestForm):

        user = await self.get_user_by_username(form_data.username)
        # Sprawdź, czy użytkownik jest zablokowany
        if user.locked_until and user.locked_until > datetime.datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is locked. Please try again later.",
            )

        hashed_pass = user.password
        if not verify_password(form_data.password, hashed_pass):
            # Aktualizuj pole login_attempts i locked_until
            if user.login_attempts >= settings.max_login_attempts:
                user.login_attempts = 0
                user.locked_until = datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=settings.lockout_duration_minutes,
                )
                await self.session.commit()
            else:
                user.login_attempts += 1
                await self.session.commit()

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthException.INCORRECT_PASSWORD,
            )

        # Zalogowano poprawnie, zresetuj login_attempts i locked_until
        user.login_attempts = 0
        user.locked_until = None

        access_token = TokenAuthentication().create_access_token(user.username, user.id)
        refresh_token = TokenAuthentication().create_refresh_token(
            user.username,
            user.id,
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            max_age=settings.expiration_access_token_max_age,
            httponly=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=settings.expiration_refresh_token_max_age,
            httponly=True,
        )

        return {"message": "Zalogowano pomyślnie"}
