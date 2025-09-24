from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class OrganizationsColumns(str, Enum):
    ENTITY = "entity"
    ID = "id"
    NAME = "name"
    EMAIL = "email"
    STATE = "state"
    TELEPHONE = "telephone"
    IS_DEFAULT = "is_default"
    TYPE = "type"
    STATUS = "status"
    WEBSITE = "website"
    CREATOR = "creator"
    CREATED_AT = "created_at"


class OrganizationStatus(str, Enum):
    ACTIVE = "Active"
    PENDING = "Pending"
    DELETED = "Deleted"


class OrganizationState(str, Enum):
    ACTIVE = "Active"
    IN_ACTIVE = "Pending"
    EXPIRED = "Expired"

class NewOrganization(BaseModel):
    name: str
    email: str
    type: str

class CreateOrganization(NewOrganization):
    id: str
    entity: str
    telephone: Optional[str] = None
    website: Optional[str] = None
    is_default: bool
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    state: OrganizationState = OrganizationState.ACTIVE
    creator: str
    created_at: datetime


class UpdateOrganization(BaseModel):
    name: str
    email: str
    type: str
    telephone: Optional[str] = None
    website: Optional[str] = None

class DeleteOrganization(BaseModel):
    status: OrganizationStatus

class Organization(CreateOrganization):
    pass


class ReadOrganization(Organization):
    pass