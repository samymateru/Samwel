from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PlanDetails(BaseModel):
    total: Optional[int] = 0
    completed: Optional[int] = 0
    pending: Optional[int] = 0
    ongoing: Optional[int] = 0

class _Engagement_(BaseModel):
    id: str
    name: str
    code: Optional[str]
    status: Optional[str]
    type: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    stage: Optional[str]


class _Issue_(BaseModel):
    id: str
    reference: Optional[str]
    title: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
    engagement: int  # Foreign key to engagement.id

class ModuleHomeDashboard(BaseModel):
    engagements: List[_Engagement_]
    issues: List[_Issue_]



