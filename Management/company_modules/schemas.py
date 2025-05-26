from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    email: str
    name: str

class Role(BaseModel):
    name: str
    user: User

class Module(BaseModel):
    id: Optional[str] = None
    name: str
    purchase_date: Optional[datetime] = None
    status: Optional[str] = None

