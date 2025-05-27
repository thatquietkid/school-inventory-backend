# app/crud/inventory.py

from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem
from app.schemas.inventory import InventoryItemCreate


def add_inventory_item(db: Session, item_data: InventoryItemCreate):
    item = InventoryItem(**item_data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_all_items(db: Session):
    return db.query(InventoryItem).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
