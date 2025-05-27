# app/api/inventory.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.inventory import InventoryItemCreate, InventoryItemResponse
from app.models.inventory import InventoryItem
from app.db.database import get_db
from app.auth.dependencies import require_role

router = APIRouter()


@router.post("/", response_model=InventoryItemResponse)
def add_item(item: InventoryItemCreate, db: Session = Depends(get_db),
             user=Depends(require_role(["Inventory Manager", "Administrator"]))):
    new_item = InventoryItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=list[InventoryItemResponse])
def list_items(db: Session = Depends(get_db),
               user=Depends(require_role(["Inventory Manager", "Administrator", "Teacher", "Maintenance Staff"]))):
    return db.query(InventoryItem).all()
