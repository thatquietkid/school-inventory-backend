from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship  # <-- make sure to import relationship here
from app.db.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # ... other columns ...

    maintenance_records = relationship("MaintenanceRecord", back_populates="item", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="item")
