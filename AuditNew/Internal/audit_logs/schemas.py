from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NewAuditLog(BaseModel):
    action: str
    description: Optional[str] = None

class UpdateAuditLog(BaseModel):
    action: Optional[str] = None
    description: Optional[str] = None
    log_id: int

class DeleteAuditLogs(BaseModel):
    log_id: List[int]

class AuditLog(BaseModel):
    log_id: int
    user_id: int
    action: str
    description: str
    created_at: str
    updated_at: str
