from app.repositories.photo_repository import create_user_photo_table

from app.repositories.photo_repository import(
    save_photo,
    get_photo,
    get_user_photos,
    delete_photo
)



def create_photo_table_for_user(user_id: int):

    return create_user_photo_table(user_id)



def upload_photo(
        user_id :int,
        filename: str,
        content_type: str,
        image_data: bytes
):
    if not content_type.startswith("image/"):
        raise ValueError("Only image files are allowed")


    if not image_data:
        raise ValueError("Image cannot be empty")

    save_photo(
        user_id=user_id,
        filename=filename,
        content_type=content_type,
        image_data=image_data
    )


def get_photos(user_id: int):

    return get_user_photos(user_id)

 
def get_single_photo(
        user_id: int,
        photo_id: int
):
    return get_photo(
        user_id=user_id,
        photo_id=photo_id
    )


def delete_single_photo(
        user_id: int,
        photo_id: int
):
    deleted_row = delete_photo(
        user_id=user_id,
        photo_id=photo_id
    )

    if deleted_row == 0:
        raise ValueError("Photo not found")

    return  {
        "message": "Photo deleted successfully"
    }




