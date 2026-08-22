from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema.users_schema import UserCreate, UserResponse,UserLogin
from app.services.users_service import register_user,authenticate_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = register_user(db, user_data)

        return user

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/authenticate")
def authenticate(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    try:
        user = authenticate_user(
            db,
            credentials.email,
            credentials.passwd
        )
        return {
            "status": "success",
            "data": {
                "uid": user.id,
                "name":user.name,
                "email":user.email,
                "mobile":user.mobile 
            }
        }
    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
   