from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.engagement_administration_profile_schemas import \
    NewEngagementAdministrationProfile


class ReportLead(BaseModel):
    email: str
    name: str


class BusinessContacts(BaseModel):
    name: str
    email: str
    role: Optional[str] = None


class EngagementReportSchema(BaseModel):
    engagement_id: str
    module_id: str
    organization_name: str
    engagement_name: str
    engagement_code: str
    engagement_leads: Optional[List[ReportLead]] = Field(default_factory=list)
    engagement_business_contacts: Optional[List[BusinessContacts]] = Field(default_factory=list)
    engagement_profile: NewEngagementAdministrationProfile




