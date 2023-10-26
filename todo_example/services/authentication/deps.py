from fastapi import Depends

from todo_example.services.authentication.auth import oauth2_scheme


def get_current_user(
    username: str = Depends(oauth2_scheme),
):
    return username
