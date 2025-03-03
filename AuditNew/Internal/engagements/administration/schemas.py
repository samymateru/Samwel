from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List

class Section(BaseModel):
    value: str

class EngagementProfile(BaseModel):
    audit_background: Optional[Section]
    audit_objectives: Optional[Section]
    key_legislations: Optional[Section]
    relevant_systems: Optional[Section]
    key_changes: Optional[Section]
    reliance: Optional[Section]
    scope_exclusion: Optional[Section]
    core_risk: Optional[List[str]]
    estimated_dates: Optional[Section]

class Policy(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    version: Optional[str]
    key_areas: Optional[str]
    attachment: Optional[str]

class EngagementProcess(BaseModel):
    id: Optional[int]
    process: Optional[str]
    sub_proces: Optional[List[str]]
    description: Optional[str]
    business_unit: Optional[str]

class Regulations(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    issue_date: Optional[datetime]
    key_areas: Optional[str]
    attachment: Optional[str]

class Role(BaseModel):
    id: int
    name: str


class Staff(BaseModel):
    id: Optional[int]
    name: Optional[str]
    role: Optional[Role]
    start_date: datetime = datetime.now()
    end_date: Optional[datetime]
    tasks: Optional[str]
