from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Optional
from enum import Enum
from utils import get_unique_key

class EngagementStatus(str, Enum):
    PENDING = "Pending"
    NOT_STARTED = "Not started"
    OPEN = "Open"
    COMPLETE = "Completed"
    CLOSED = "Closed"
    ONGOING = "Ongoing"

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

class Role(BaseModel):
    name: Optional[str]

class Risk(BaseModel):
    name: str
    magnitude: int

class Lead(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    email: Optional[str]
    role: Optional[str] = None

class Engagement(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    type: Optional[str]
    code: Optional[str] = None
    risk: Optional[Risk]
    leads: Optional[List[Lead]]
    quarter: Optional[str] = None
    department: Optional[Department]
    sub_departments: Optional[List[str]]
    status: EngagementStatus = EngagementStatus.PENDING
    stage: EngagementStage = EngagementStage.NOT_STARTED
    start_date: Optional[datetime] = datetime.now()
    end_date: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now()

class UpdateEngagement(BaseModel):
    name: str
    risk: Optional[Risk]
    type: str
    department: Optional[Department]
    sub_departments: Optional[List[str]]


class DeleteEngagements(BaseModel):
    engagement_id: List[str]


class Rating(BaseModel):
    maturity_rating: str
    rationale: str

class RiskMaturityRating(BaseModel):
    engagement_id: str
    operational_risk: Rating
    strategic_risk: Rating
    credit_risk: Rating
    liquidity_risk: Rating
    compliance_risk: Rating
    market_risk: Rating
    overall: Rating


#------------------------------------------------------------------
class NewEngagement(BaseModel):
    name: str
    type: str
    risk: str
    leads: List[str]
    department: str
    sub_department: List[str]
    start_date: datetime
    end_date: datetime

class CreateEngagement(BaseModel):
    id: str
    plan_id: str
    name: str
    code: str
    type: str
    risk: str
    department: str
    sub_department: List[str]
    start_date: datetime
    end_date: datetime
    status: EngagementStatus
    stage: EngagementStage
    created_by: Optional[str] = None
    created_at: datetime



