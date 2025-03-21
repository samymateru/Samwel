from pydantic import BaseModel
from typing import List, Dict, Optional

class Permissions(BaseModel):
    annual_audit_plan: List[str]
    engagements: List[str]
    administration: List[str]
    planning: List[str]
    fieldwork: List[str]
    finalization: List[str]
    reporting: List[str]
    work_program: List[str]

class Role(BaseModel):
    id: Optional[int] = None
    name: str
    permissions: Permissions
