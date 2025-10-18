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
    USER_ID = "user_id"


class Stage(BaseModel):
    hours: int
    start_date: str
    end_date: str

class NewStage(BaseModel):
    hours: int
    start_date: datetime
    end_date: datetime




class NewEngagementStaff(BaseModel):
    user_id: str
    name:  str
    email: str
    role: str
    role_id: str
    planning: NewStage
    fieldwork: NewStage
    reporting: NewStage
    finalization: NewStage


class CreateEngagementStaff(BaseModel):
    id: str
    engagement: str
    user_id: str
    name: str
    email: str
    role: str
    role_id: str
    planning: Stage
    fieldwork: Stage
    reporting: Stage
    finalization: Stage
    created_at: datetime


class BaseEngagementStaff(CreateEngagementStaff):
    pass


class ReadEngagementStaff(BaseEngagementStaff):
    pass



class UpdateStaff(BaseModel):
    role: str
    role_id: str
    planning: Stage
    fieldwork: Stage
    reporting: Stage
    finalization: Stage
