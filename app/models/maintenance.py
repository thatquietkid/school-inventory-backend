from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    maintenance_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=False)
    performed_by = Column(String, nullable=True)
    status = Column(String, default="pending")

    item = relationship("app.models.inventory.InventoryItem", back_populates="maintenance_records")
