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


class Stage(BaseModel):
    hours: int
    start_date: datetime
    end_date: datetime



class NewEngagementStaff(BaseModel):
    name:  str
    email: str
    role: str
    role_id: str
    planning: Stage
    fieldwork: Stage
    reporting: Stage
    finalization: Stage


class CreateEngagementStaff(NewEngagementStaff):
    id: str
    engagement: str
    created_at: datetime



class ReadEngagementStaff(CreateEngagementStaff):
    pass



class UpdateStaff(BaseModel):
    role: str
    role_id: str
    planning: Stage
    fieldwork: Stage
    reporting: Stage
    finalization: Stage
