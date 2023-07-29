from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import models, schemas

hero_model = models.Hero


def create_hero(request: schemas.HeroRequest, db: Session):
    new_hero = hero_model(
        main_text=request.main_text,
        alt_text=request.alt_text,
    )
    db.add(new_hero)
    db.commit()
    db.refresh(new_hero)

    return new_hero

def show_hero(db: Session):
    hero = db.query(hero_model).first()

    if not hero:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} is not found",
        )

    return hero


def edit_hero(id: UUID4, request: schemas.HeroRequest, db: Session):
    edited_hero = request.dict(exclude_unset=True)
    hero = db.query(hero_model).filter(hero_model.id == id)

    if not hero.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id {id} is not found",
        )

    hero.update(edited_hero, synchronize_session=False)
    db.commit()

    return {"detail": "Hero was updated"}
