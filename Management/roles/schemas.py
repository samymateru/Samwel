from pydantic import BaseModel
from typing import List
from enum import Enum

class Actions(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ASSIGN = "assign"
    APPROVE = "approve"

class Permissions(BaseModel):
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
    permissions: Permissions

class Role(BaseModel):
    roles: List[Category]


