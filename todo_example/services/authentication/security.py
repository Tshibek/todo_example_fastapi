import uuid

from todo_example.services.authentication.manager import TokenManager
from todo_example.settings import settings


class TokenAuthentication(TokenManager):
    def create_access_token(self, username: str, object_id: uuid.UUID):
        return self._create_token(username, object_id, settings.expiration_access_token)

    def create_refresh_token(
        self,
        username: str,
        object_id: uuid.UUID,
        refresh_count: int = 0,
    ):
        return self._create_token(
            username,
            object_id,
            settings.expiration_refresh_token,
            refresh_count,
        )

    def verify_token(self, token: str):
        decoded = self._verify_token(token)
        return decoded
