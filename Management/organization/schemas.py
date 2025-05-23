from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime

class OrganizationStatus(str, Enum):
    ACTIVE = "Active"
    IN_ACTIVE = "In active"
    OPENED = "Opened"

class Organization(BaseModel):
    id: Optional[str] = None
    name: str
    owner: str
    email: str
    telephone: str
    default: bool
    type: str
    status: OrganizationStatus
    website: str
    created_at: datetime = datetime.now()

