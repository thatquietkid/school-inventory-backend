# app/api/booking.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.booking import BookingCreate, BookingResponse
from app.models.booking import Booking
from app.db.database import get_db
from app.auth.dependencies import require_role

router = APIRouter()

@router.post("/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db),
                   user=Depends(require_role(["Teacher", "Administrator"]))):
    db_booking = Booking(**booking.dict(), user_id=user["id"])
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


@router.get("/", response_model=list[BookingResponse])
def list_bookings(db: Session = Depends(get_db),
                  user=Depends(require_role(["Administrator", "Teacher", "Inventory Manager"]))):
    return db.query(Booking).all()
