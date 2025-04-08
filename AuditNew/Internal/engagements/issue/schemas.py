from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class User(BaseModel):
    name: str
    email: str

class Issue(BaseModel):
    id: Optional[int] = None
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

class IssueContacts(BaseModel):
    LOD1_implementer: Optional[List[User]]
    LOD1_owner: Optional[List[User]]
    LOD2_risk_manager: Optional[List[User]]
    LOD2_compliance_officer: Optional[List[User]]
    LOD3_audit_manager: Optional[List[User]]
    observers: Optional[List[User]]

class IssueStatus(BaseModel):
    implementer_status: Optional[str] = None
    owner_status: Optional[str] = None
    owner_comments: Optional[str] = None
    risk_manager_status: Optional[str] = None
    compliance_officer_status: Optional[str] = None


class NewIssue(BaseModel):
    title: str