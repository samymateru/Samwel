from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class EngagementStatus(str, Enum):
    NOT_STARTED = "Not started"
    OPEN = "Open"
    COMPLETE = "Complete"
    CLOSED = "Closed"

class EngagementPhase(str, Enum):
    ADMINISTRATION = "Administration"
    PLANNING = "Planning"
    FIELDWORK = "Fieldwork"
    REPORTING = "Reporting"
    FINALIZATION = "Finalization"

class Engagement(BaseModel):
    engagement_id: int
    annual_plan_id: int
    engagement_name: str
    engagement_code: str
    engagement_risk: str
    engagement_type: str
    engagement_lead: str
    engagement_status: str
    engagement_phase: str
    quarter: str

class NewEngagement(BaseModel):
    engagement_name: str
    engagement_risk: str
    engagement_type: str
    template_id: int
    engagement_status: EngagementStatus = EngagementStatus.NOT_STARTED
    engagement_phase: EngagementPhase = EngagementPhase.ADMINISTRATION
    quarter: str = "1"
    start_date: datetime = None
    end_date: datetime = None
    created_at: datetime = datetime.now()

class UpdateEngagement(BaseModel):
    engagement_id: int
    engagement_name: str = None
    engagement_risk: str = None
    engagement_type: str = None
    engagement_lead: str = None
    engagement_status: EngagementStatus = None
    engagement_phase: EngagementPhase = None
    quarter: str = None
    start_date: datetime = None
    end_date: datetime = None
    updated_at: datetime = datetime.now()

class DeleteEngagements(BaseModel):
    engagement_id: List[int]


