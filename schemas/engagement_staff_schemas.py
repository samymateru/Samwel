from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class EngagementRoles(str, Enum):
    pass


class NewEngagementStaff(BaseModel):
    name:  str
    email: str
    role: EngagementRoles
    start_date: datetime
    end_date: datetime
    tasks: str


class CreateEngagementStaff(NewEngagementStaff):
    id: str
    engagement: str
    name:  str
    email: str
    role: EngagementRoles
    start_date: datetime
    end_date: datetime
    tasks: str


class UpdateStaff(BaseModel):
    role: str
    start_date: datetime
    end_date: datetime
    tasks: datetime