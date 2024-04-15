import io
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from app.utils.resources_handle import download_image


async def get_images(image_name: str):
    try:
        image_content, media_type = download_image(image_name)
        return StreamingResponse(io.BytesIO(image_content), media_type=media_type)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
