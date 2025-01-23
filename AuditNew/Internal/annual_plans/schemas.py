from pydantic import BaseModel
from datetime import datetime
from enum import  Enum
from typing import Optional, List

class AnnualPlansStatus(str, Enum):
    NOT_STARTED = "Not Started"
    PROGRESS = "In progress"
    COMPLETED = "Completed"

class NewAnnualPlan(BaseModel):
    name: str
    year: Optional[str] = datetime.now().year
    created_at: Optional[datetime] = datetime.now()
    status:  AnnualPlansStatus = AnnualPlansStatus.NOT_STARTED
    description: Optional[str] = None
    audit_type: str = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

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

