from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import datetime

class EngagementColumns(str, Enum):
    ID = "id"
    PLAN_ID = "plan_id"
    MODULE_ID = "module_id"
    NAME = "name"
    STATUS = "status"
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
    ARCHIVED = "Archived"


class EngagementStage(str, Enum):
    PENDING = "Pending"
    NOT_STARTED = "Not Started"
    ADMINISTRATION = "Administration"
    PLANNING = "Planning"
    FIELDWORK = "Fieldwork"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"


class Risk(BaseModel):
    name: str
    magnitude: int


class Lead(BaseModel):
    id: str
    name: str
    email: str
    role: str


class Department(BaseModel):
    name: str
    code: str


class NewEngagement(BaseModel):
    name: str
    type: str
    risk: Risk
    leads: List[Lead]
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
    archived: bool
    start_date: datetime
    end_date: datetime
    created_at: datetime


#--------------------------------------------------------------


class UpdateEngagement_(BaseModel):
    name: str
    type: str
    risk: Risk
    department: Department
    sub_departments: List[str]
    start_date: datetime
    end_date: datetime

class UpdateEngagement(BaseModel):
    name: str
    type: str
    risk: str
    department: Department
    sub_departments: List[str]
    start_date: datetime
    end_date: datetime


#---------------------------------------------------------------


class AddOpinionRating(BaseModel):
    opinion_rating: str


class ArchiveEngagement(BaseModel):
    archived: bool
    status: EngagementStatus


class CompleteEngagement(BaseModel):
    status: EngagementStatus


class DeleteEngagementPartially(BaseModel):
    status: EngagementStatus


class Engagement(CreateEngagement):
    pass


class ReadEngagement(Engagement):
    leads: List[Lead]
