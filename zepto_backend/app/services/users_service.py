from sqlalchemy.orm import Session
from app.services.photo_service import create_photo_table_for_user
from app.repositories.users_repository import (
    create_user,
    get_user_by_email,
    find_user_by_credentials
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


def authenticate_user(
    db,
    email: str,
    password: str
):
    user = find_user_by_credentials(
        db,
        email,
        password
    )

    if user is None:
        raise ValueError(
            "Invalid email or password"
        )
    return user