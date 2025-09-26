from pydantic import BaseModel
from enum import Enum
from typing import Dict, Optional
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