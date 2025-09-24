from pydantic import BaseModel
from typing import Dict
from datetime import datetime
from enum import Enum


class LibraryCategory(str, Enum):
    RISK_CONTROLS = "Risks & Controls"
    AUDIT_PROGRAM = "Audit Program"
    PROGRAM_PROCEDURE = "Program Procedure"
    STANDARD_PROCEDURE = "Standard Procedure"


class RiskControlItem(BaseModel):
    risk: str
    risk_rating: str
    control: str
    control_objective: str
    control_type: str
    residual_risk: str


class LibraryColumns(str, Enum):
    LIBRARY_ID = "library_id"
    MODULE_ID = "module_id"
    name = "name"
    category = "category"
    data = "data"
    created_by = "created_by"
    approved_by = "approved_by"
    created_at = "created_at"


class NewLibraryItem(BaseModel):
    name: str
    category: LibraryCategory
    data: Dict

class CreateLibraryItem(BaseModel):
    library_id: str
    module_id: str
    name: str
    category: str
    data: Dict
    created_by: str
    approved_by: str
    created_at: datetime


