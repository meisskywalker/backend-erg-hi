from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from .. import db, schemas, models
from app import oauth2
from ..handlers import hero

get_db = db.get_db

router = APIRouter(prefix="/hero", tags=["Hero"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.HeroRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return hero.create_hero(request, db)


@router.get("/", status_code=status.HTTP_200_OK)
def show(
    db: Session = Depends(get_db),
):
    return hero.show_hero(db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: UUID4,
    request: schemas.HeroRequest,
    db: Session = Depends(get_db),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return hero.edit_hero(id, request, db)
