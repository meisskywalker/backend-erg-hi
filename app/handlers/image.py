import os
import shutil
import uuid
from fastapi import HTTPException, status

from fastapi.responses import FileResponse

IMAGEDIR = "./images"
SLIDESDIR = f"{IMAGEDIR}/slides"


def check_file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)


async def upload_image(file):
    os.makedirs(IMAGEDIR, exist_ok=True)

    _, ext = os.path.splitext(str(file.filename))
    file.filename = f"image-{uuid.uuid4()}{ext}"
    content = await file.read()

    with open(f"{IMAGEDIR}/{file.filename}", "wb") as buffer:
        buffer.write(content)

    return {"filename": file.filename}


async def upload_slides(files):
    shutil.rmtree(SLIDESDIR)
    os.makedirs(SLIDESDIR, exist_ok=True)

    for file in files:
        _, ext = os.path.splitext(str(file.filename))
        file.filename = f"slide-{uuid.uuid4()}{ext}"
        content = await file.read()

        with open(f"{SLIDESDIR}/{file.filename}", "wb") as buffer:
            buffer.write(content)

    return {"detail": "Slides were updated"}


def get_slides():
    slides = os.listdir(SLIDESDIR)
    return slides


def get_image(filename: str, slides = False):
    if not slides:
        file_path = f"./images/{filename}"
        return FileResponse(file_path)
    else:
        file_path = f"{SLIDESDIR}/{filename}"
        return FileResponse(file_path)


def delete_image(filename):
    if check_file_exists(IMAGEDIR, filename):
        os.remove(f"{IMAGEDIR}/{filename}")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with name {filename} is not found",
        )

    return {"detail": "File was deleted"}
