from pydantic import BaseModel
from typing import List, Dict, Optional

class SubCategory(BaseModel):
    name: str
    permissions: Dict[str, List[str]]

class NewRole(BaseModel):
    name: str
    creator: Optional[str]
    categories: List[SubCategory]

class Role(BaseModel):
    id: int
    roles: NewRole

class Permission(BaseModel):
    user_roles: List[str]
    subscription: List[str]


class Roles(BaseModel):
    id: Optional[int] = None
    name: str
    permissions: Permission
