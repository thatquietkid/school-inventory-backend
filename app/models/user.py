from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # <-- This must be defined
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    bookings = relationship("Booking", back_populates="user")