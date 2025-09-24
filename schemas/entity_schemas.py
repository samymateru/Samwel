from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class EntitiesColumns(str, Enum):
    ID = "id"
    NAME = "name"
    OWNER = "owner"
    EMAIL = "email"
    TELEPHONE = "telephone"
    STATUS = "status"
    CREATOR = "creator"
    CREATED_AT = "created_at"


class EntitiesStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"


class NewEntity(BaseModel):
    name: str
    owner: str
    email: str
    type: str
    password: str


class CreateEntity(BaseModel):
    id: str
    name: str
    owner: str
    email: str
    website: Optional[str] = None
    telephone: Optional[str] = None
    created_at: datetime
    status: EntitiesStatus = EntitiesStatus.ACTIVE


class UpdateCreator(BaseModel):
    creator: str

class UpdateEntity(BaseModel):
    name: str
    email: str
    website: Optional[str] = None
    telephone: Optional[str] = None

class ReadEntity(BaseModel):
    id: str
    name: str
    owner: str
    email: str
    status: str
    telephone: Optional[str] = None
    created_at: datetime


