from pydantic import BaseModel
from typing import Optional


class ImpactCategory(BaseModel):
    id: int
    impact_category_name: str
    impact_sub_category_name: str

class NewImpactCategory(BaseModel):
    id: Optional[int] = None
    name: str

class NewImpactSubCategory(BaseModel):
    id: Optional[int] = None
    name: str