from sqlalchemy.orm import Session
from app.services.photo_service import create_photo_table_for_user
from app.repositories.users_repository import (
    create_user,
    get_user_by_email
)

def register_user(db: Session, user_data):


    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        raise ValueError("Email already registered")

    if user_data.password != user_data.confirmPassword:
        raise ValueError("Passwords do not match")

    user = create_user(db, user_data)
    create_photo_table_for_user(user.id)
    return user