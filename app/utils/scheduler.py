# app/utils/scheduler.py

from sqlalchemy.orm import Session
from app.models.booking import Booking

def is_conflict(db: Session, resource_id: int, start_time, end_time) -> bool:
    overlapping = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.end_time > start_time,
        Booking.start_time < end_time
    ).first()
    return overlapping is not None
