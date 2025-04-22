from pydantic import BaseModel
from typing import Optional, List


class ImpactCategory(BaseModel):
    id: int
    impact_category: str
    impact_sub_category: str

class NewImpactCategory(BaseModel):
    id: Optional[int] = None
    name: str

class NewImpactSubCategory(BaseModel):
    id: Optional[int] = None
    name: str

class CombinedImpactCategory(BaseModel):
    process_name: str
    sub_process_name: List[str]