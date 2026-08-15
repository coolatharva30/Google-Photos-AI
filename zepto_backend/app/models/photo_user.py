from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    LargeBinary,
    DateTime,
    MetaData
)
from sqlalchemy.sql import func

def create_photo_model(user_id: int):

    table_name = f"user_{user_id}_photos"

    metadata = MetaData()

    photo_table = Table (
        table_name,
        metadata,

        Column(
            "id",
            Integer,
            primary_key=True,
            autoincrement=True
        ),

        Column(
            "filename",
            String(255),
            nullable=False
        ),

        Column(
            "content_type",
            String(100),
            nullable=False
        ),

        Column(
            "image_data",
            LargeBinary,
            nullable=False
        ),

        Column(
            "created_at",
            DateTime,
            server_default=func.now()
        )
     )

    return photo_table