from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class NewCompanyModule(BaseModel):
    module_id: int
    is_active: Optional[bool] = True


class UpdateCompanyModule(BaseModel):
    company_module_id: int
    module_id: Optional[int] = None
    is_active: Optional[bool] = None

class DeleteCompanyModule(BaseModel):
    company_module_id: List[int]
