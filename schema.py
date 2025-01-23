from pydantic import BaseModel
from typing import Optional

class CurrentUser(BaseModel):
    user_id: Optional[int] = None
    company_id: Optional[int] = None
    role_id: Optional[int] = None
    type: Optional[str] = None
    status_code: Optional[int] = None
    description: Optional[str] = None

class TokenError(BaseModel):
    status_code: int
    description: str