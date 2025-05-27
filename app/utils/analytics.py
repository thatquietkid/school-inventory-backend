# app/utils/analytics.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.booking import Booking

def most_booked_resources(db: Session, days: int = 30):
    start_date = datetime.utcnow() - timedelta(days=days)
    results = (
        db.query(Booking.resource_id, func.count(Booking.id).label("bookings"))
        .filter(Booking.start_time >= start_date)
        .group_by(Booking.resource_id)
        .order_by(func.count(Booking.id).desc())
        .all()
    )
    return results

def resource_usage_trend(db: Session, resource_id: int, days: int = 30):
    start_date = datetime.utcnow() - timedelta(days=days)
    results = (
        db.query(func.date(Booking.start_time), func.count(Booking.id))
        .filter(Booking.resource_id == resource_id)
        .filter(Booking.start_time >= start_date)
        .group_by(func.date(Booking.start_time))
        .all()
    )
    return results
