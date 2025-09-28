from pydantic import BaseModel
from enum import Enum
from typing import Dict, Optional, List
from datetime import datetime



class LibraryColumns(str, Enum):
    LIBRARY_ID = "library_id"
    MODULE_ID = "module_id"
    NAME = "name"
    CATEGORY = "category"
    DATA = "data"
    CREATED_BY = "created_by"
    CREATED_AT = "created_at"


class LibraryCategory(str, Enum):
    MAIN_PROGRAM = "Main Program"
    SUB_PROGRAM = "Sub Program"
    RISK_CONTROL = "Risk Control"
    WORKING_PAPER = "Working Paper"


class CreateLibraryEntry(BaseModel):
    library_id: str
    module_id: str
    name: Optional[str]
    category: LibraryCategory
    data: Dict
    created_by: str
    created_at: datetime


class ImportLibraryItems(BaseModel):
    library_ids: List[str]




class RiskControlLibraryItem(BaseModel):
    risk: str
    risk_rating: str
    control: str
    control_type: str
    control_objective: str



class SubProgramLibraryItem(BaseModel):
    prcm: List[RiskControlLibraryItem]
    title: str
    test_type: str
    audit_objective: str
    test_description: str
    brief_description: str
    sampling_approach: str



class MainProgramLibraryItem(BaseModel):
    program_name: str
    program_description: str
    sub_programs: List[SubProgramLibraryItem]


class LibraryItemUpdate(BaseModel):
    data: Dict






