from pydantic import BaseModel, RootModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class ProgramSummary(BaseModel):
    id: Optional[str] = None
    name: str
    status: Optional[str]
    process_rating: Optional[str]
    issue_count: int
    acceptable: int
    improvement_required: int
    significant_improvement_required: int
    unacceptable: int
    recurring_issues: int


class User(BaseModel):
    name: Optional[str]
    email: Optional[str]
    date_issued: Optional[datetime]

class IssueActors(str, Enum):
    IMPLEMENTER = "lod1_implementer"
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"

class IssueStatus(str, Enum):
    NOT_STARTED = "Not started"
    OPEN = "Open"
    IN_PROGRESS_IMPLEMENTER = "In progress -> implementer"
    IN_PROGRESS_OWNER = "In progress -> owner"
    CLOSED_NOT_VERIFIED = "Closed -> not verified"
    CLOSED_VERIFIED_BY_RISK = "Closed -> verified by risk"
    CLOSED_RISK_NA = "Closed -> risk N/A"
    CLOSED_RISK_ACCEPTED = "Closed -> risk accepted"
    CLOSED_VERIFIED_BY_AUDIT = "Closed -> verified by audit"

class ResponseActors(str, Enum):
    OWNER = "lod1_owner"
    RISK_MANAGER = "lod2_risk_manager"
    COMPLIANCE_OFFICER = "lod2_compliance_officer"
    AUDIT_MANAGER = "lod3_audit_manager"

class LOD2Feedback(str, Enum):
    CLOSED_VERIFIED_BY_RISK = "Closed -> verified by risk"
    CLOSED_RISK_NA = "Closed -> risk N/A"
    CLOSED_RISK_ACCEPTED = "Closed -> risk accepted"


class IssueCounts(BaseModel):
    total: int
    very_high_risk: int
    moderate_risk: int
    recurring_count: int


class SubProgram(BaseModel):
    sub_program_id: str
    title: str
    effectiveness: Optional[str] = None
    issue_counts: IssueCounts
    total_very_high_risk: int
    total_moderate_risk: int
    total_recurring_issues: int


class MainProgram(BaseModel):
    main_program_id: str
    program: str
    sub_programs: List[SubProgram]


# Root model for a list of MainProgram
class EngagementPrograms(RootModel[List[MainProgram]]):
    pass