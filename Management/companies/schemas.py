from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum
from  utils import get_unique_key

class UserType(str, Enum):
    ADMINISTRATOR = "administrator",
    USER = "user"


class Module(BaseModel):
    id: Optional[int] = None
    name: str
    purchase_date: Optional[datetime] = None
    status: Optional[str] = None


class Company(BaseModel):
    id: Optional[str]
    name: str
    owner: str
    email: str
    telephone: str
    website: Optional[str] = None
    entity_type: str
    status: str
    created_at: datetime

class NewCompany(BaseModel):
    id: str = Field(default_factory=get_unique_key)
    name: str
    owner: str
    email: str
    telephone: str
    website:  Optional[str]
    password: str
    entity_type: str
    status: Optional[str] = "setup"
    modules: Optional[List[Module]]