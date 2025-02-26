from pydantic import BaseModel
from typing import List, Dict

class NewRole(BaseModel):
    name: str
    categories: Dict[str, List[str]]

class Role(BaseModel):
    id: int
    roles: NewRole


