from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class User(BaseModel):
    id: int
    name: str
    email: str

class MainProgram(BaseModel):
    id: Optional[int] = None
    name: Optional[str]

class SubProgram(BaseModel):
    id: Optional[int] = None
    reference: Optional[str] = None
    title: Optional[str]
    brief_description: Optional[str]
    audit_objective: Optional[str]
    test_description: Optional[str]
    test_type: Optional[str]
    sampling_approach: Optional[str]
    results_of_test: Optional[str]
    observation: Optional[str]
    extended_testing: Optional[bool]
    extended_procedure: Optional[str]
    extended_results: Optional[str]
    effectiveness: Optional[str]
    conclusion: Optional[str]
    evidence: List[str]

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
    implementation_contacts: Optional[str]

class Task(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    reference: Optional[str]
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    action_owner: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[str]
    date_resolved: Optional[datetime]
    decision: Optional[str]


class ReviewNote(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    reference: Optional[str]
    description: Optional[str]
    date_raised: Optional[datetime]
    raised_by: Optional[User]
    action_owner: Optional[User]
    resolution_summary: Optional[str]
    resolution_details: Optional[str]
    resolved_by: Optional[str]
    date_resolved: Optional[datetime]
    decision: Optional[str]
