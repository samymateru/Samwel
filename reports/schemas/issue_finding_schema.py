from datetime import datetime
from typing import Dict, Optional, List
from pydantic import BaseModel

from schemas.engagement_administration_profile_schemas import ReadEngagementAdministrationProfile


class ResponsiblePeople(BaseModel):
    id: str
    name: str
    email: str
    role: str
    title: str
    mod_usr_role : Optional[str] = None



class IssuesFinding(BaseModel):
    title: str
    criteria: Dict
    finding: Dict
    risk_rating: str
    source: str
    process: str
    sub_process: str
    root_cause: str
    sub_root_cause: str
    risk_category: str
    sub_risk_category: str
    impact_category: str
    impact_sub_category: str
    root_cause_description: Dict
    impact_description: Dict
    recommendation: Dict
    management_action_plan: Optional[Dict] | Optional[str] = None
    recurring_status: Optional[bool] = False
    estimated_implementation_date: datetime
    responsible_people: List[ResponsiblePeople]



class EngagementReport(BaseModel):
    organization_name: str
    engagement_name: str
    engagement_code: str
    engagement_profile: ReadEngagementAdministrationProfile
    issues: List[IssuesFinding]