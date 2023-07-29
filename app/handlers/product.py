import os
from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

import models, schemas
import tf_idf

product_model = models.Product

IMAGEDIR = "./images"

def check_file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)

def show_products(db: Session, page: int = 1, limit: int = 10):
    total_count = db.query(product_model).count()
    has_more = (page * limit) < total_count

    if limit <= 0:
        return {"data": db.query(product_model).all()}
    else:
        return {
            "data": db.query(product_model)
            .offset((page - 1) * limit)
            .limit(limit)
            .all(),
            "total": total_count,
            "has_more": has_more,
        }


def show_product(id: UUID4, db: Session):
    product = db.query(product_model).filter(product_model.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} is not found",
        )

    return product


def show_tf_idf(query: str, db: Session):
    corpus = {a.id: a.title for a in show_products(db)["data"]}
    df = tf_idf.Tf_Idf(corpus)
    tfidf = df.val_tfidf

    keywords = df.clean_w(query)
    match_w = list(filter(lambda w: w in list(tfidf.T.columns), keywords))
    found = tfidf.T.loc[:, match_w]
    return found.T.sum().to_dict()


def create_product(request: schemas.ProductRequest, db: Session):
    new_product = models.Product(
        title=request.title,
        description=request.description,
        filename=request.filename,
        video_link=request.video_link,
        demo_link=request.demo_link,
        journal_link=request.journal_link,
        author=request.author,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


def edit_product(id: UUID4, request: schemas.ProductRequest, db: Session):
    edited_product = request.dict(exclude_unset=True)
    product = db.query(product_model).filter(product_model.id == id)

    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} is not found",
        )

    product.update(edited_product, synchronize_session=False)
    db.commit()

    return {"detail": "Product was updated"}


def delete_product(id: UUID4, db: Session):
    product = db.query(product_model).filter(product_model.id == id)

    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} is not found",
        )

    filename = product.first().filename
    if check_file_exists(IMAGEDIR, filename):
        os.remove(f"{IMAGEDIR}/{filename}")

    product.delete(synchronize_session=False)
    db.commit()

    return {"detail": "Product was deleted"}
