from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import shutil
import uuid
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary directory to store uploaded images
TEMP_DIR = Path("temp_images")
TEMP_DIR.mkdir(exist_ok=True)  # Creates the folder if it doesn't exist


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/upload")
async def upload_image(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    """
    Uploads an image file and returns the filename
    """

    ALLOWED_TYPES = (
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
        "image/tiff",
    )
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate a unique ID and secure filename
    image_id = str(uuid.uuid4())
    file_extension = file.filename.split(".")[-1]
    filename = f"{image_id}.{file_extension}"

    file_path = TEMP_DIR / filename

    # Save the file to disk
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not save file")
    finally:
        file.file.close()

    # Return filename and image ID
    return {"filename": filename, "imageId": image_id}
