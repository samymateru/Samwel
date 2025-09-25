from pydantic import BaseModel
from typing import Optional, Dict, List
from enum import Enum


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
    audit_background: Dict
    audit_objectives: Dict
    key_legislations: Dict
    relevant_systems: Dict
    key_changes: Dict
    reliance: Dict
    scope_exclusion: Dict
    core_risk: Optional[List[str]] = None


class CreateEngagementAdministrationProfile(NewEngagementAdministrationProfile):
    id: str
    engagement: str


class ReadEngagementAdministrationProfile(CreateEngagementAdministrationProfile):
    pass