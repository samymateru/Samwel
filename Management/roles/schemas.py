from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Actions(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ASSIGN = "assign"
    APPROVE = "approve"

class Permission(BaseModel):
    annual_audit_plan: List[Actions]
    engagements: List[Actions]
    administration: List[Actions]
    planning: List[Actions]
    fieldwork: List[Actions]
    finalization: List[Actions]
    reporting: List[Actions]
    work_program: List[Actions]

class Category(BaseModel):
    name: str
    permissions: Permission

class Role(BaseModel):
    roles: List[Category]


###################################################

class Permissions(str, Enum):
    VIEW = "view"
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    APPROVE = "approve"
    REVIEW = "review"

class RolesSections(str, Enum):
    SETTINGS = "settings"
    AUDIT_PLAN = "audit_plans"
    ADMINISTRATION = "administration"
    PLANNING = "planning"
    FIELDWORK = "fieldwork"
    REPORTING = "reporting"
    AUDIT_PROGRAM = "audit_program"
    FOLLOW_UP = "follow_up"
    ISSUE_MANAGEMENT = "issue_management"
    ARCHIVE_AUDIT = "archive_audit"
    UN_ARCHIVE_AUDIT = "un_archive_audit"
    OTHERS = "others"

class Section(str, Enum):
    E_AUDIT = "e_audit"
    ENGAGEMENT = "engagement"

class Archive(str, Enum):
    YES = "yes"
    NO = "no"

class Type(str, Enum):
    BUSINESS = "business"
    AUDIT = "audit"

class Default(str, Enum):
    YES = "yes"
    NO = "no"

class Roles(BaseModel):
    id: Optional[str] = None
    reference: Optional[str] = None
    default: Default = Default.NO
    name: Optional[str]
    section: Optional[Section] = Section.E_AUDIT
    type: Type
    settings: List[Permissions] = Field(default_factory=list)
    audit_plans: List[Permissions] = Field(default_factory=list)
    engagements: List[Permissions] = Field(default_factory=list)
    administration: List[Permissions]  = Field(default_factory=list)
    planning: List[Permissions]  = Field(default_factory=list)
    fieldwork: List[Permissions]  = Field(default_factory=list)
    finalization: List[Permissions]  = Field(default_factory=list)
    reporting: List[Permissions]  = Field(default_factory=list)
    audit_program: List[Permissions]  = Field(default_factory=list)
    follow_up: List[Permissions]  = Field(default_factory=list)
    issue_management: List[Permissions]  = Field(default_factory=list)
    archive_audit: Archive = Archive.NO
    un_archive_audit: Archive = Archive.NO
    others: List[Permissions]  = Field(default_factory=list)
    created_at: Optional[datetime] = datetime.now()

class EditRole(BaseModel):
    name: Optional[str]
    section: Optional[Section] = Section.E_AUDIT
    type: Type
    settings: List[Permissions] = Field(default_factory=list)
    audit_plans: List[Permissions] = Field(default_factory=list)
    engagements: List[Permissions] = Field(default_factory=list)
    administration: List[Permissions] = Field(default_factory=list)
    planning: List[Permissions] = Field(default_factory=list)
    fieldwork: List[Permissions] = Field(default_factory=list)
    finalization: List[Permissions]  = Field(default_factory=list)
    reporting: List[Permissions] = Field(default_factory=list)
    audit_program: List[Permissions] = Field(default_factory=list)
    follow_up: List[Permissions] = Field(default_factory=list)
    issue_management: List[Permissions] = Field(default_factory=list)
    archive_audit: Archive = Archive.NO
    un_archive_audit: Archive = Archive.NO
    others: List[Permissions] = Field(default_factory=list)