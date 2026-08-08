from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SENIOR_DEV = "senior_dev"
    JUNIOR_DEV = "junior_dev"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.JUNIOR_DEV)
