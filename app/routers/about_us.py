from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from .. import db, schemas, models
from app import oauth2
from ..handlers import about_us

get_db = db.get_db

router = APIRouter(prefix="/about-us", tags=["About Us"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.AboutUsRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return about_us.create_about_us(request, db)


@router.get("/", status_code=status.HTTP_200_OK)
def show(
    db: Session = Depends(get_db),
):
    return about_us.show_about_us(db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: UUID4,
    request: schemas.AboutUsRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return about_us.edit_about_us(id, request, db)
