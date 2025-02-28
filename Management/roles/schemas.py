from pydantic import BaseModel
from typing import List, Dict

class SubCategory(BaseModel):
    name: str
    permissions: Dict[str, List[str]]

class NewRole(BaseModel):
    name: str
    creator: str
    categories: List[SubCategory]

class Role(BaseModel):
    id: int
    roles: NewRole
