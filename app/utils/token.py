from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

import schemas


def create_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )

    return encoded_jwt


def verify_token(token: str, credential_exception):
    try:
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get("ALGORITHM")]
        )
        email = payload.get("sub")
        if email is None:
            raise credential_exception

        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credential_exception
