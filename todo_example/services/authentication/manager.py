import json
import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from pyseto import Key, pyseto

from todo_example.settings import settings
from todo_example.utils.enums.exceptions import AuthException


class TokenManager:
    def __init__(self):
        self.private_key = Key.new(
            version=4,
            purpose="public",
            key=settings.private_key_pem,
        )
        self.public_key = Key.new(
            version=4,
            purpose="public",
            key=settings.public_key_pem,
        )

    def _create_token(
        self,
        object_username: str,
        object_id: uuid.UUID,
        expires_delta: int,
        refresh_count: int = None,
    ):
        payload_dict = {
            "date": {"id": str(object_id), "username": object_username},
            "exp": (datetime.utcnow() + timedelta(minutes=expires_delta)).timestamp(),
        }
        if refresh_count is not None:
            payload_dict["refresh_count"] = refresh_count

        token = pyseto.encode(
            self.private_key,
            json.dumps(payload_dict).encode("utf-8"),
        )
        return token.decode()

    def _decode_token(self, token: str):
        try:
            payload_dict = pyseto.decode(self.public_key, token)
            payload_data = json.loads(payload_dict.payload.decode("utf-8"))
            return payload_data
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def _verify_token(self, token: str):
        payload_data = self._decode_token(token)
        if datetime.utcnow().timestamp() > payload_data.get("exp", 0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=AuthException.VERIFY_TOKEN_EXPIRED,
            )
        try:
            if payload_data.get("refresh_count") > settings.max_refresh_token_count:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=AuthException.VERIFY_TOKEN_EXPIRED,
                )
        except Exception:
            pass

        return payload_data
