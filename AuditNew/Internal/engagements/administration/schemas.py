from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional

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

class Policy(BaseModel):
    id: Optional[int]
    name: str
    version: str
    key_areas: Section
    attachment: str

class EngagementProcess(BaseModel):
    id: Optional[int]
    process: str
    sub_proces: Any
    description: str
    business_unit: str

class Regulations(BaseModel):
    id: Optional[int]
    name: str
    issue_date: datetime
    ke_areas: str
    attachment: str

class Role(BaseModel):
    id: int
    name: str


class Staff(BaseModel):
    id: Optional[int]
    name: str
    role: Role
    start_date: datetime
    end_date: datetime
    tasks: Any
