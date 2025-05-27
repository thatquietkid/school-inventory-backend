# app/schemas/maintenance.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MaintenanceRequestBase(BaseModel):
    item_id: int
    issue_description: str
    reported_by: str


class MaintenanceRequestCreate(MaintenanceRequestBase):
    pass


class MaintenanceRequestResponse(MaintenanceRequestBase):
    id: int
    status: str  # e.g., "Pending", "In Progress", "Resolved"
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        orm_mode = True
