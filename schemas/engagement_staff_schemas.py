from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class EngagementStaffColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"
    ROLE_ID = "role_id"


class Stage(BaseModel):
    hours: int
    start_date: str
    end_date: str



class NewEngagementStaff(BaseModel):
    user_id: str
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
