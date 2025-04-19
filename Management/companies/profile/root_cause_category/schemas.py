from pydantic import BaseModel
from typing import List, Optional

class RootCauseCategory(BaseModel):
    id: Optional[int] = None
    name: str
    company: str

class CombinedRootCauseCategory(BaseModel):
    process_name: str
    sub_process_name: List[str]