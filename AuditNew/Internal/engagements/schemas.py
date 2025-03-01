from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Any
from enum import Enum

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
    id: int
    name: str

class Risk(BaseModel):
    name: str
    magnitude: int

class Lead(BaseModel):
    name: str
    user_id: int
    role: Role

class Engagement(BaseModel):
    engagement_id: int
    annual_plan_id: int
    engagement_name: str
    engagement_code: str
    engagement_risk: Risk
    engagement_type: str
    engagement_lead: List[Lead]
    engagement_status: str
    engagement_phase: str
    quarter: str

class NewEngagement(BaseModel):
    engagementName: str
    engagementType: str
    engagementRisk: Risk
    engagementLead: List[Lead]
    plannedQuarter: str
    department: Department
    sub_department: List[str]
    status: EngagementStatus = EngagementStatus.NOT_STARTED
    stage: EngagementStage = EngagementStage.NOT_STARTED
    startDate: datetime = None
    endDate: datetime = None
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
    engagement_id: List[int]
