from fastapi import HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer

from todo_example.services.authentication.security import TokenAuthentication
from todo_example.settings import settings
from todo_example.utils.enums.exceptions import AuthException


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    def __init__(self, tokenUrl="/api/users/login"):
        super().__init__(tokenUrl=tokenUrl)

    async def __call__(self, request: Request, response: Response):
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token:
            payload = TokenAuthentication().verify_token(access_token)
            return payload.get("date")

        if refresh_token:
            refresh_token_payload = TokenAuthentication().verify_token(refresh_token)
            refresh_count = int(refresh_token_payload.get("refresh_count"))

            if refresh_count < settings.max_refresh_token_count:
                response.delete_cookie("refresh_token")
                new_access_token = TokenAuthentication().create_access_token(
                    username=refresh_token_payload.get("date").get("username"),
                    object_id=refresh_token_payload.get("date").get("id"),
                )
                refresh_count += 1
                new_refresh_token = TokenAuthentication().create_refresh_token(
                    username=refresh_token_payload.get("date").get("username"),
                    object_id=refresh_token_payload.get("date").get("id"),
                    refresh_count=refresh_count,
                )

                response.set_cookie(
                    key="access_token",
                    value=new_access_token,
                    max_age=settings.expiration_access_token_max_age,
                    httponly=True,
                    samesite="strict",
                )

                response.set_cookie(
                    key="refresh_token",
                    value=new_refresh_token,
                    max_age=settings.expiration_refresh_token_max_age,
                    httponly=True,
                    samesite="strict",
                )
                print(refresh_token_payload)
                return refresh_token_payload.get("sub")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=AuthException.VERIFY_USER_BAD_TOKEN,
        )


oauth2_scheme = CustomOAuth2PasswordBearer()
