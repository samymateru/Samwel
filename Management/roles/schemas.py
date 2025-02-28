from pydantic import BaseModel
from typing import List, Dict

class SubCategory(BaseModel):
    name: str
    categories: Dict[str, List[str]]

class NewRole(BaseModel):
    name: str
    sub_categories: List[SubCategory]

class Role(BaseModel):
    id: int
    roles: NewRole
