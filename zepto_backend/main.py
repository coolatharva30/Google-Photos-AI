from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.users_router import router as user_router

# Import models so SQLAlchemy knows about them
from app.models.users import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(user_router, prefix="/users")


@app.get("/")
def home():
    return {"message": "FastAPI is running"}