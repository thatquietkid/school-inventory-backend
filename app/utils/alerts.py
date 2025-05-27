# app/utils/alerts.py

from datetime import date
from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem

LOW_STOCK_THRESHOLD = 5

def get_low_stock_items(db: Session):
    return db.query(InventoryItem).filter(InventoryItem.quantity < LOW_STOCK_THRESHOLD).all()

def get_expired_items(db: Session):
    today = date.today()
    return db.query(InventoryItem).filter(InventoryItem.expiry_date != None).filter(InventoryItem.expiry_date < today).all()
