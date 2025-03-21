from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Issue(BaseModel):
    id: Optional[int] = None
    ref: Optional[str]
    title: Optional[str]
    criteria: Optional[str]
    finding: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
    sub_process: Optional[str]
    root_cause_description: Optional[str]
    root_cause: Optional[str]
    sub_root_cause: Optional[str]
    risk_category: Optional[str]
    sub_risk_category: Optional[str]
    impact_description: Optional[str]
    impact_category: Optional[str]
    impact_sub_category: Optional[str]
    recurring_status: Optional[bool]
    recommendation: Optional[str]
    management_action_plan: Optional[str]
    estimated_implementation_date: Optional[datetime]
    implementation_contacts: Optional[str]

class NewIssue(BaseModel):
    title: str