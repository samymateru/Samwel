from pydantic import BaseModel, Field
from datetime import datetime
from enum import  Enum
from typing import Optional, List

class AnnualPlansStatus(str, Enum):
    NOT_STARTED = "Not Started"
    PENDING = "Pending"
    ON_GOING = "Ongoing"
    COMPLETED = "Completed"


class AnnualPlan(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    module: Optional[str] = None
    name: str
    year: Optional[str] = str(datetime.now().year)
    status: AnnualPlansStatus = AnnualPlansStatus.PENDING
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    attachment: str
    created_at: Optional[datetime] = datetime.now()

class NewAnnualPlan(BaseModel):
    name: str
    year: Optional[str] = str(datetime.now().year)

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

