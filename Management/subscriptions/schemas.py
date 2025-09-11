from pydantic import BaseModel

class EAuditLicence(BaseModel):
    licence_id: str
    name: str
    audit_staff: int
    business_staff: int
    engagements_count: int
    issues_count: int
    email_count: int
    follow_up: bool
    price: int

class ERiskLicence(BaseModel):
    licence_id: str
    name: str
    risk_staff: int
    business_staff: int
    engagements_count: int
    issues_count: int
    email_count: int
    follow_up: bool