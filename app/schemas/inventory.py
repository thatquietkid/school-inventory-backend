# app/schemas/inventory.py

from pydantic import BaseModel
from datetime import date
from typing import Optional


class InventoryItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    quantity: int
    location: Optional[str] = None
    expiry_date: Optional[date] = None


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemResponse(InventoryItemBase):
    id: int
    added_on: date

    class Config:
        orm_mode = True
