from pydantic import BaseModel, Field
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
    email: str
    telephone: str
    default: Optional[bool] = Field(default=False)
    type: str
    status: Optional[OrganizationStatus] = Field(default=OrganizationStatus.OPENED)
    website: str
    created_at: datetime = datetime.now()

