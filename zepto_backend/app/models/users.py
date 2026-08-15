from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users_1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    mobile = Column(String(15), nullable=False)

