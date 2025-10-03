from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class ReportType(str, Enum):
    DRAFT_ENGAGEMENT_REPORT = "draft_engagement_report"
    DRAFT_ENGAGEMENT_LETTER = "draft_engagement_letter"
    DRAFT_FINDING_LETTER = "draft_finding_sheet"


class ReportsColumns(str, Enum):
    REPORT_ID = "report_id"
    MODULE_ID = "module_id"
    ENGAGEMENT_ID = "engagement_id"
    ENGAGEMENT_NAME = "engagement_name"
    ENGAGEMENT_CODE = "engagement_code"
    PLAN_NAME = "plan_name"
    PLAN_YEAR = "plan_year"
    URL = "url"
    FILE_NAME = "file_name"
    FILE_SIZE = "file_size"
    FILE_TYPE = "file_type"
    CATEGORY = "category"



class Reports(BaseModel):
    report_id: str
    module_id: str
    engagement_id: str
    engagement_name: str
    engagement_code: str
    plan_name: str
    plan_year: str
    url: str
    file_name: str
    file_size: int
    file_type: str
    category: ReportType
    created_at: datetime

