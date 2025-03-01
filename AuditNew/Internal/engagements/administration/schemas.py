from datetime import datetime
from pydantic import BaseModel
from typing import Any, Optional, List

class Section(BaseModel):
    value: str

class EngagementProfile(BaseModel):
    audit_background: Optional[Section] = None
    audit_objectives: Optional[Section] = None
    key_legislations: Optional[Section] = None
    relevant_systems: Optional[Section] = None
    key_changes: Optional[Section] = None
    reliance: Optional[Section] = None
    scope_exclusion: Optional[Section] = None
    core_risk: Optional[List[str]] = None
    estimated_dates: Optional[Section] = None

class Policy(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    version: Optional[str] = None
    key_areas: Optional[Section] = None
    attachment: Optional[str] = None

class EngagementProcess(BaseModel):
    id: Optional[int] = None
    process: Optional[str] = None
    sub_proces: Optional[List[str]] = None
    description: Optional[str] = None
    business_unit: Optional[str] = None

class Regulations(BaseModel):
    id: Optional[int]
    name: Optional[str] = None
    issue_date: Optional[datetime] = None
    key_areas: Optional[str] = None
    attachment: Optional[str] = None

class Role(BaseModel):
    id: int
    name: str


class Staff(BaseModel):
    id: Optional[int]
    name: Optional[str] = None
    role: Optional[Role] = None
    start_date: datetime = datetime.now()
    end_date: Optional[datetime] = None
    tasks: Optional[Any] = None
