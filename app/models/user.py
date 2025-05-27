# app/models/user.py

from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., "Administrator", "Teacher", etc.
    bookings = relationship("Booking", back_populates="user")