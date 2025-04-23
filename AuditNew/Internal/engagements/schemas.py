from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Optional
from enum import Enum
from utils import get_unique_key

class EngagementStatus(str, Enum):
    NOT_STARTED = "Not started"
    OPEN = "Open"
    COMPLETE = "Complete"
    CLOSED = "Closed"

class EngagementStage(str, Enum):
    NOT_STARTED = "Not Started"
    ADMINISTRATION = "Administration"
    PLANNING = "Planning"
    FIELDWORK = "Fieldwork"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"

class Department(BaseModel):
    name: str
    code: str

class Role(BaseModel):
    name: Optional[str]

class Risk(BaseModel):
    name: str
    magnitude: int

class Lead(BaseModel):
    name: Optional[str]
    email: Optional[str]
    user_id: Optional[str]
    role: List[Role]

class Engagement(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    type: Optional[str]
    code: Optional[str]
    risk: Optional[Risk]
    leads: Optional[List[Lead]]
    quarter: Optional[str] = None
    department: Optional[Department]
    sub_departments: Optional[List[str]]
    status: EngagementStatus = EngagementStatus.NOT_STARTED
    stage: EngagementStage = EngagementStage.NOT_STARTED
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = datetime.now()

class UpdateEngagement(BaseModel):
    engagement_id: int
    engagement_name: str = None
    engagement_risk: str = None
    engagement_type: str = None
    engagement_lead: str = None
    engagement_status: EngagementStatus = None
    engagement_phase: EngagementStage = None
    quarter: str = None
    start_date: datetime = None
    end_date: datetime = None
    updated_at: datetime = datetime.now()

class DeleteEngagements(BaseModel):
    engagement_id: List[str]
