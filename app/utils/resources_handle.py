import os
from pathlib import Path
import shutil
import uuid
from fastapi import HTTPException, UploadFile, status


async def upload_image(file: UploadFile):
    UPLOAD_PATH = Path("app/api/v1/uploads")

    if file is None:
        raise Exception("No file uploaded.")

    if not UPLOAD_PATH.exists():
        UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

    try:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise ValueError("Invalid file type, only JPEG and PNG files are allowed.")

        # Extracting file extension
        file_extension = Path(file.filename).suffix.lower() if file.filename else ""

        # Generating a unique filename with the file extension
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = Path(f"{UPLOAD_PATH}/{file_name}")

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return f"{file_name}"

    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def download_image(filename: str):
    UPLOAD_PATH = Path("app/api/v1/uploads")

    file_path = UPLOAD_PATH / filename
    file_extension = filename.split(".")[-1]

    if not file_path.exists():
        raise FileNotFoundError("File not found")

    if file_extension.lower() == "jpeg" or file_extension.lower() == "jpg":
        media_type = "image/jpeg"
    elif file_extension.lower() == "png":
        media_type = "image/png"
    else:
        raise Exception("Invalid file type")

    with open(file_path, "rb") as file:
        return file.read(), media_type
