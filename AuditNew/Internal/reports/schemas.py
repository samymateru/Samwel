from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from schemas.issue_schemas import IssueStatus



class ReportIssues(BaseModel):
    reference: str
    created_at: datetime
    latest_response: Optional[str] = None
    reportable: Optional[bool] = False
    issue_name: str
    issue_criteria: str
    finding: str
    risk_rating: str
    issue_source: str
    process: str
    sub_process: str
    root_cause_description: str
    impact_description: str
    recommendation: str
    estimated_implementation_date: datetime
    sdi_name: Optional[str] = None
    recurring_status: Optional[bool] = False
    management_action_plan: Optional[str]  = None


    issue_overall_status: IssueStatus
    issue_due_more_than_365_days: Optional[str]
    issue_due_more_than_90_days: Optional[str] = None
    days_remaining_to_implementation: Optional[int] = None
    is_issue_pass_due: str
    issue_revised_count: Optional[int] = 0
    actual_implementation_date: Optional[datetime] = None
    latest_revised_date: Optional[datetime] = None
    is_issue_revised: str


