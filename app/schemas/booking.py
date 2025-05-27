# app/schemas/booking.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BookingBase(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    booked_by: str  # username or user ID
    created_at: datetime

    class Config:
        orm_mode = True
