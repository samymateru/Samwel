from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import datetime

class EngagementColumns(str, Enum):
    ID = "id"
    PLAN_ID = "plan_id"
    MODULE_ID = "module_id"
    NAME = "name"
    CODE = "code"
    TYPE = "type"
    CREATED_AT = "created_at"


class EngagementStatus(str, Enum):
    PENDING = "Pending"
    NOT_STARTED = "Not started"
    OPEN = "Open"
    COMPLETED = "Completed"
    CLOSED = "Closed"
    ONGOING = "Ongoing"
    DELETED = "Deleted"


class EngagementStage(str, Enum):
    PENDING = "Pending"
    NOT_STARTED = "Not Started"
    ADMINISTRATION = "Administration"
    PLANNING = "Planning"
    FIELDWORK = "Fieldwork"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"


class Department(BaseModel):
    name: str
    code: str


class NewEngagement(BaseModel):
    name: str
    type: str
    risk: str
    leads: List[str]
    department: Department
    sub_departments: List[str]
    start_date: datetime
    end_date: datetime


class CreateEngagement(BaseModel):
    id: str
    plan_id: str
    module_id: str
    name: str
    type: str
    code: str
    risk: str
    quarter: str
    department: Department
    sub_departments: List[str]
    status: EngagementStatus
    stage: EngagementStage
    start_date: datetime
    end_date: datetime
    created_at: datetime


class UpdateEngagement(BaseModel):
    pass


class AddOpinionRating(BaseModel):
    opinion_rating: str


class ArchiveEngagement(BaseModel):
    archived: bool


class CompleteEngagement(BaseModel):
    status: EngagementStatus


class DeleteEngagementPartially(BaseModel):
    status: EngagementStatus

class Engagement(CreateEngagement):
    pass

class ReadEngagement(Engagement):
    pass