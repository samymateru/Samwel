from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum



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
    telephone: Optional[str] = ""
    type: str
    website: Optional[str] = ""
    password: str



#----------------------------------------------------------------------------#


#-------------------------------------------------------------------------------
