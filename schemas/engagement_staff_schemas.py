from typing import Optional

from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class EngagementStaffColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"
    START_DATE = "start_date"
    END_DATE = "end_date"
    TASKS = "tasks"



class NewEngagementStaff(BaseModel):
    name:  str
    email: str
    role: str
    start_date: datetime
    end_date: datetime
    tasks: Optional[str] = None


class CreateEngagementStaff(NewEngagementStaff):
    id: str
    engagement: str
    name:  str
    email: str
    role: str
    start_date: datetime
    end_date: datetime
    tasks: Optional[str] = None


class ReadEngagementStaff(CreateEngagementStaff):
    pass


class UpdateStaff(BaseModel):
    role: str
    start_date: datetime
    end_date: datetime
    tasks: Optional[str] = None