from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Section(BaseModel):
    value: str

class EngagementProfile(BaseModel):
    id: Optional[str] = None
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
    id: Optional[str] = None
    name: Optional[str]
    version: Optional[str]
    key_areas: Optional[str]
    attachment: Optional[str]

class EngagementProcess(BaseModel):
    id: Optional[str] = None
    process: Optional[str]
    sub_process: Optional[List[str]]
    description: Optional[str]
    business_unit: Optional[str]

class Regulations(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    issue_date: Optional[datetime]
    key_areas: Optional[str]
    attachment: Optional[str]

class Staff(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    start_date: datetime = datetime.now()
    end_date: Optional[datetime]
    tasks: Optional[str] = None

class User(BaseModel):
    id: str
    name: str
    email: str

class BusinessContact(BaseModel):
    id: Optional[str] = None
    user: List[User]
    type: Optional[str]
