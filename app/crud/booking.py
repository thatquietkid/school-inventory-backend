# app/crud/booking.py

from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate


def create_booking(db: Session, booking_data: BookingCreate, booked_by: str):
    booking = Booking(**booking_data.dict(), booked_by=booked_by)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_all_bookings(db: Session):
    return db.query(Booking).all()


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()
