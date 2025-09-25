from pydantic import BaseModel
from typing import Optional, Dict, List

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
    created_at: str


class ReadEngagementAdministrationProfile(CreateEngagementAdministrationProfile):
    pass