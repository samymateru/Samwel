from pydantic import BaseModel, Field
from datetime import datetime
from enum import  Enum
from typing import Optional, List
from utils import get_unique_key

class AnnualPlansStatus(str, Enum):
    NOT_STARTED = "Not Started"
    PENDING = "Pending"
    ON_GOING = "Ongoing"
    COMPLETED = "Completed"


class AnnualPlan(BaseModel):
    id: str = Field(default_factory=get_unique_key)
    name: str
    year: Optional[str] = datetime.now().year
    status: AnnualPlansStatus = AnnualPlansStatus.PENDING
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    attachment: str
    created_at: Optional[datetime] = datetime.now()

class NewAnnualPlan(BaseModel):
    name: str
    year: Optional[str] = datetime.now().year
    status: AnnualPlansStatus = AnnualPlansStatus.PENDING
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    file: str
    created_at: Optional[datetime] = datetime.now()

class DeleteAnnualPlan(BaseModel):
    plan_id: List[int]

class UpdateAnnualPlan(BaseModel):
    annual_plan_id: int
    name: Optional[str] = None
    year: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    audit_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

