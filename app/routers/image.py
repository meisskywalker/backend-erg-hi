import os
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status
from .. import schemas
from .. import oauth2
from ..handlers import image

router = APIRouter(prefix="/images", tags=["Images"])

IMAGEDIR = "./images"


def check_file_exists(directory, filename):
    file_path = os.path.join(directory, filename)
    return os.path.isfile(file_path)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return await image.upload_image(file)


@router.post("/slides", status_code=status.HTTP_201_CREATED)
async def upload_slides(
    files: List[UploadFile] = File(...),
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return await image.upload_slides(files)

@router.get("/slides")
def get_slides():
    return image.get_slides()

@router.get("/slides/{filename}")
async def get_slides_image(filename: str):
    return image.get_image(filename, slides=True)


@router.get("/{filename}")
async def get_file(filename: str):
    return image.get_image(filename)


@router.delete("/{filename}", status_code=status.HTTP_200_OK)
async def remove_file(
    filename: str,
    current_user: schemas.UserRequest = Depends(oauth2.get_current_user),
):
    return image.delete_image(filename)
