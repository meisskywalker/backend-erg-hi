from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import schemas

from app.handlers import user

from .. import db

get_db = db.get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", status_code=status.HTTP_200_OK)
def show_by_id(id: UUID4, db: Session = Depends(get_db)):
    return user.show_user(id, db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.UserRequest, db: Session = Depends(get_db)):
    return user.create_user(request, db)
