from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from .. import db, schemas, models
from app import oauth2
from ..handlers import contact_us

get_db = db.get_db

router = APIRouter(prefix="/contact-us", tags=["Contact Us"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.ContactUsRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return contact_us.create_contact_us(request, db)


@router.get("/", status_code=status.HTTP_200_OK)
def index(db: Session = Depends(get_db)):
    return contact_us.show_contact_uses(db)


@router.get("/{id}", status_code=status.HTTP_200_OK)
def show(
    id: UUID4,
    db: Session = Depends(get_db),
):
    return contact_us.show_contact_us(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: UUID4,
    request: schemas.ContactUsRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return contact_us.edit_contact_us(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def destroy(
    id: UUID4,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return contact_us.delete_contact_us(id, db)
