from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from schemas.issue_actor_schemas import ReadIssueActors
from schemas.issue_schemas import IssueStatus


class ReportIssues(BaseModel):
    id:str
    ref: str
    engagement_name: str
    engagement_code: str
    engagement_opinion_rating: Optional[str] = None
    plan_year: str
    response: Optional[str] = None
    reportable: Optional[bool] = False
    title: str
    criteria: str
    finding: str
    risk_rating: str
    source: str
    process: str
    sub_process: str
    root_cause_description: str
    impact_description: str
    recommendation: str
    estimated_implementation_date: datetime
    sdi_name: Optional[str] = None
    recurring_status: Optional[bool] = False
    management_action_plan: Optional[str]  = None
    status: IssueStatus
    created_at: datetime
    date_revised: datetime
    revised_count: Optional[int] = 0
    revised_status: Optional[bool] = False
    implementers: List[ReadIssueActors]



    # issue_due_more_than_365_days: Optional[str]
    # issue_due_more_than_90_days: Optional[str] = None
    # days_remaining_to_implementation: Optional[int] = None
    # is_issue_pass_due: str
    # issue_revised_count: Optional[int] = 0
    # actual_implementation_date: Optional[datetime] = None
    # latest_revised_date: Optional[datetime] = None
    # is_issue_revised: str


