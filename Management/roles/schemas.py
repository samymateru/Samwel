from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Role(BaseModel):
    name: str
    description: str
    category: str
    write: bool
    read: bool
    edit: bool
    assign: bool
    approve: bool
    delete: bool

class NewRole(BaseModel):
    name: str
    description: str
    category: str
    write: bool
    read: bool
    edit: bool
    assign: bool
    approve: bool
    delete: bool
    created_at: datetime = datetime.now()



class DeleteRoles(BaseModel):
    roles_id: List[int]

class UpdateRole(BaseModel):
    role_name: Optional[str] = None
    description: Optional[str] = None
    role_id: int

