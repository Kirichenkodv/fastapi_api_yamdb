from datetime import datetime, timedelta
from typing import Union

import jwt

from settings import path_settings

# >>> private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
# >>> public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


def encode_jwt(
    payload: dict,
    private_key: str = path_settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = path_settings.auth_jwt.algorithm,
    expire_minutes: int = path_settings.auth_jwt.access_token_expire_minutes,
    # expire_timedelta: timedelta | None = None,
    expire_timedelta: Union[timedelta, None] = None
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: Union[str, bytes],
    public_key: str = path_settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = path_settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded
