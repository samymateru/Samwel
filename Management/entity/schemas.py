from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum
from  utils import get_unique_key

class Module(BaseModel):
    id: Optional[int] = None
    name: str
    purchase_date: Optional[datetime] = None
    status: Optional[str] = None


class Entity(BaseModel):
    id: Optional[str]
    name: str
    owner: str
    email: str
    telephone: str
    status: bool
    created_at: datetime

class NewEntity(BaseModel):
    name: str
    owner: str
    email: str
    telephone: str
    type: str
    website: str
    password: str