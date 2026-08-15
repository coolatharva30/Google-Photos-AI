from app.database import engine
from app.models.photo_user import create_photo_model


def create_user_photo_table(user_id: int):

    photo_table = create_photo_model(user_id)

    photo_table.metadata.create_all(engine)

    return photo_table


