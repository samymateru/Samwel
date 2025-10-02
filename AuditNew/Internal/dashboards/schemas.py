from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PlanDetails(BaseModel):
    total: Optional[int] = 0
    completed: Optional[int] = 0
    pending: Optional[int] = 0
    ongoing: Optional[int] = 0

class _EngagementStatus_(BaseModel):
    total: int
    pending: int
    ongoing: int
    completed: int
    archived: int
    deleted: int

class _IssueStatus_(BaseModel):
    pending: int
    ongoing: int
    completed: int



class IssueStatusSummary(BaseModel):
    total: int
    not_started: int
    open: int
    in_progress: int
    closed: int

class _Engagement_(BaseModel):
    id: Optional[str]
    name: Optional[str]
    code: Optional[str]
    status: Optional[str]
    type: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    stage: Optional[str]

class _Issue_(BaseModel):
    id: Optional[str]
    reference: Optional[str]
    title: Optional[str]
    risk_rating: Optional[str]
    process: Optional[str]
    status: Optional[str] = None
    engagement: str

class ModuleHomeDashboard(BaseModel):
    engagements_metrics: _EngagementStatus_
    issues_metrics: IssueStatusSummary


class EngagementMetrics(BaseModel):
    total: int
    pending: int
    ongoing: int
    completed: int








