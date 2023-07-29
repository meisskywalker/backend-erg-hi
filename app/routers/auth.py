from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models
from ..utils import token
from ..utils.hash import Hash

from .. import db

get_db = db.get_db
user_model = models.User

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(user_model).filter(user_model.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    if not Hash.verify_hased_text(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )

    access_token = token.create_token(data={"sub": user.email})
    response.set_cookie(key="token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}
