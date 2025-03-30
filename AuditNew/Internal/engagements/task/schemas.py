from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    name: str
    email: str

class Task(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    reference: Optional[str]
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    action_owner: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[User]
    date_resolved: Optional[datetime]
    decision: Optional[str]

class NewTask(BaseModel):
    title: str