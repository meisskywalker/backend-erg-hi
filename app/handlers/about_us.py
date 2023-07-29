from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session
from app import models, schemas

about_us_model = models.AboutUs


def create_about_us(request: schemas.AboutUsRequest, db: Session):
    new_about_us = about_us_model(
        filename=request.filename,
        text=request.text,
        description=request.description,
    )
    db.add(new_about_us)
    db.commit()
    db.refresh(new_about_us)

    return new_about_us


def show_about_us(db: Session):
    about_us = db.query(about_us_model).first()

    if not about_us:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"About Us with id {id} is not found",
        )

    return about_us


def edit_about_us(id: UUID4, request: schemas.AboutUsRequest, db: Session):
    edited_about_us = request.dict(exclude_unset=True)
    about_us = db.query(about_us_model).filter(about_us_model.id == id)

    if not about_us.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"About Us with id {id} is not found",
        )

    about_us.update(edited_about_us, synchronize_session=False)
    db.commit()

    return {"detail": "About Us was updated"}
