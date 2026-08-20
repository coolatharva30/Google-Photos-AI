from app.database import engine
from app.models.photo_user import create_photo_model
from sqlalchemy import insert,select

def create_user_photo_table(user_id: int):

    photo_table = create_photo_model(user_id)

    photo_table.metadata.create_all(engine)

    return photo_table


def save_photo(
        user_id: int,
        filename: str,
        content_type: str,
        image_data: bytes
):

    photo_table = create_photo_model(user_id)

    with engine.connect() as connection:

        statement = insert(photo_table).values(
            filename=filename,
            content_type=content_type,
            image_data=image_data
        )
        connection.execute(statement)
        connection.commit()
        

def get_user_photos(user_id: int):

    photo_table = create_photo_model(user_id)

    with engine.connect() as connection:

        statement = select(
            photo_table.c.id,
            photo_table.c.filename,
            photo_table.c.content_type,
            photo_table.c.created_at
        )

    result = connection.execute(statement)

    return result.mappings().all()

def get_photo(
        user_id: int,
        photo_id: int
):

    photo_table = create_photo_model(user_id)

    with engine.connect() as connection:

        statement = select(
            photo_table
        ).where(
            photo_table.c.id == photo_id
        )

        result = connection.execute(statement)

        return result.mappings().first()


    
    
    



