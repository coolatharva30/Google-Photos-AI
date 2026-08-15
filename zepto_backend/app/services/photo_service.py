from app.repositories.photo_repository import create_user_photo_table

def create_photo_table_for_user(user_id: int):

    return create_user_photo_table(user_id)


