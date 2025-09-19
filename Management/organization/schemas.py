from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime



class OrganizationStatus(str, Enum):
    ACTIVE = "Active"
    IN_ACTIVE = "Pending"
    EXPIRED = "Expired"


class Organization(BaseModel):
    id: str
    name: str
    email: str
    telephone: Optional[str] = None
    default: bool = Field(default=False)
    type: str
    status: Optional[bool] = True
    website: Optional[str] = None
    administrator: Optional[bool] = False
    owner: Optional[bool] = False
    created_at: datetime = datetime.now()

class UpdateOrganization(BaseModel):
    name: str
    email: str
    telephone: str
    default: Optional[bool] = Field(default=False)
    type: str

class NewOrganization(BaseModel):
    name: str
    email: str
    telephone: Optional[str] = None
    website: Optional[str] = None
    type: str

