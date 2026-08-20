from sqlalchemy.orm import Session
from app.models.users import User


def create_user(db: Session, user_data):
    user = User(
        name = user_data.name,
        email=user_data.email,
        password=user_data.password,
        mobile=user_data.mobile
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def find_user_by_credentials(
        db:Session,
        email: str,
        password: str
):
    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.password == password
        ).first()
    )

    return user







    
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
