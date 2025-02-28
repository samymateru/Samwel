from pydantic import BaseModel
from typing import Any

class Section(BaseModel):
    value: str

class EngagementProfile(BaseModel):
    audit_background: Section
    audit_objectives: Section
    key_legislations: Section
    relevant_systems: Section
    key_changes: Section
    reliance: Section
    scope_exclusion: Section
    core_risk: Any
    estimated_dates: Any


