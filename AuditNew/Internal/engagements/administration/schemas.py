from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict
from enum import Enum


class BusinessUserType(str, Enum):
    ACTION = "Action"
    INFORMATION = "Information"


class EngagementProfile(BaseModel):
    id: Optional[str] = None
    audit_background: Optional[Dict]
    audit_objectives: Optional[Dict]
    key_legislations: Optional[Dict]
    relevant_systems: Optional[Dict]
    key_changes: Optional[Dict]
    reliance: Optional[Dict]
    scope_exclusion: Optional[Dict]
    core_risk: Optional[List[str]]

class Policy(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    version: Optional[str]
    key_areas: Optional[str]
    attachment: Optional[str] = None

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
    user_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    start_date: datetime = datetime.now()
    end_date: Optional[datetime]
    tasks: Optional[str] = None

class __Staff__(BaseModel):
    id: Optional[str] = None
    name: Optional[str]
    email: Optional[str]
    role: Optional[str]
    start_date: datetime = datetime.now()
    end_date: Optional[datetime]
    tasks: Optional[str] = None

class User(BaseModel):
    name: str
    email: str

class BusinessContact(BaseModel):
    id: Optional[str] = None
    user: List[User]
    type: Optional[BusinessUserType]
