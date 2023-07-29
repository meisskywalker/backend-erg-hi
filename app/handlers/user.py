from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.hash import Hash

user_model = models.User


def show_user(id: UUID4, db: Session):
    user = db.query(user_model).filter(user_model.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not found",
        )

    return user


def create_user(request: schemas.UserRequest, db: Session):
    hashed_pwd = Hash.hash_text(request.password)
    new_user = user_model(
        username=request.username, email=request.email, password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user.id
