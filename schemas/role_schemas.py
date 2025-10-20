from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from datetime import datetime


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
    ENGAGEMENT = "engagements"
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


class RoleColumns(str, Enum):
    ID = "id"
    MODULE = "module"
    NAME = "name"
    REFERENCE = "reference"
    DEFAULT = "default"
    SECTION = "section"
    TYPE = "type"
    SETTINGS = "settings"
    AUDIT_PLANS = "audit_plans"
    ENGAGEMENTS = "engagements"
    ADMINISTRATION = "administration"
    PLANNING = "planning"
    FIELDWORK = "fieldwork"
    FINALIZATION = "finalization"
    REPORTING = "reporting"
    AUDIT_PROGRAM = "audit_program"
    FOLLOW_UP = "follow_up"
    ISSUE_MANAGEMENT = "issue_management"
    ARCHIVE_AUDIT = "archive_audit"
    UN_ARCHIVE_AUDIT = "un_archive_audit"
    OTHERS = "others"
    HEAD = "head"
    CREATED_AT = "created_at"



class NewRole(BaseModel):
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



class CreateRole(NewRole):
    id: str
    reference: str
    module: Optional[str] = None
    default: Default
    head: bool = False
    created_at: datetime


class UpdateRole(NewRole):
    pass


class BaseRole(CreateRole):
    pass


class ReadRole(BaseRole):
    pass




