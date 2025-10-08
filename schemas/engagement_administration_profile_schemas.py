from pydantic import BaseModel
from typing import Optional, Dict, List
from enum import Enum


class PrepareReview(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    date_issued: Optional[str] = None


class EngagementProfileColumns(str, Enum):
    ID = "id"
    ENGAGEMENT = "engagement"
    AUDIT_BACKGROUND = "audit_background"
    AUDIT_OBJECTIVES = "audit_objectives"
    KEY_LEGISLATIONS = "key_legislations"
    RELEVANT_SYSTEMS = "relevant_systems"
    KEY_CHANGES = "key_changes"
    RELIANCE = "reliance"
    SCOPE_EXCLUSION = "scope_exclusion"
    CORE_RISK = "core_risk"


class NewEngagementAdministrationProfile(BaseModel):
    audit_background: Optional[Dict] = None
    audit_objectives: Optional[Dict] = None
    key_legislations: Optional[Dict] = None
    relevant_systems: Optional[Dict] = None
    key_changes: Optional[Dict]
    reliance: Optional[Dict]
    scope_exclusion: Optional[Dict]
    core_risk: Optional[List[str]] = None


class CreateEngagementAdministrationProfile(NewEngagementAdministrationProfile):
    id: str
    engagement: str



class ReadEngagementAdministrationProfile(CreateEngagementAdministrationProfile):
    reviewed_by: Optional[PrepareReview] = None
    prepared_by: Optional[PrepareReview] = None


class ReviewEngagementProfile(BaseModel):
    reviewed_by: PrepareReview


class PrepareEngagementProfile(BaseModel):
    prepared_by: PrepareReview