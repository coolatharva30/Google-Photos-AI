from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import Response

from app.services.photo_service import (
    upload_photo,
    get_photos,
    get_single_photo,
    delete_single_photo
)

from app.schema.photo_schema import PhotoResponse

router = APIRouter(
    tags=["Photos"]
)

@router.post("/upload")
async def upload(
    user_id: int,
    latitude: float | None = None,
    longitude: float | None = None,
    file: UploadFile = File(...)
):
    try:
        image_data = await file.read()

        upload_photo(
            user_id=user_id,
            filename=file.filename,
            content_type=file.content_type,
            image_data=image_data,
            latitude=latitude,
            longitude=longitude
        )

        return {
            "status": "success",
            "message": "Photo uploaded successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/")
def get_all_photos(
    user_id: int
):

    photos = get_photos(user_id)

    return {
        "status": "success",
        "data": photos
    }


@router.get("/{photo_id}")
def get_image(
    photo_id: int,
    user_id: int
):

    photo = get_single_photo(
        user_id=user_id,
        photo_id=photo_id
    )

    if not photo:

        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )

    return Response(
        content=photo["image_data"],
        media_type=photo["content_type"]
    )

@router.delete("/{photo_id}")
def delete_photo(
    photo_id: int,
    user_id: int
):
    try:
        return delete_single_photo(
            user_id=user_id,
            photo_id=photo_id
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )