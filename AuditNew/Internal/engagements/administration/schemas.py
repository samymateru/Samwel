from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Section(BaseModel):
    value: str

class EngagementProfile(BaseModel):
    id: Optional[int] = None
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
    id: Optional[int] = None
    process: Optional[str]
    sub_process: Optional[List[str]]
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
    id: Optional[int] = None
    name: Optional[str]
    role: Optional[Role]
    start_date: datetime = datetime.now()
    end_date: Optional[datetime]
    tasks: Optional[str]

class User(BaseModel):
    id: int
    name: str
    email: str

class BusinessContact(BaseModel):
    id: Optional[int] = None
    user: List[User]
    type: Optional[str]
