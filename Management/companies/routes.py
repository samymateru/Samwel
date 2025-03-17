from fastapi import APIRouter, Depends, HTTPException, Query
from Management.users.databases import add_user_module
from utils import get_db_connection
from Management.companies.schemas import *
from Management.users.schemas import Module
from Management.company_modules.schemas import CompanyModule
from Management.company_modules.databases import add_new_company_module
from typing import Tuple, List, Dict
from Management.companies import databases as company_database
from Management.users.databases import new_user
from schema import CurrentUser, ResponseMessage
from utils import generate_hash_password, get_current_user
from Management.companies import databases
from Management.users.schemas import *
from seedings import *
router = APIRouter(prefix="/companies")

@router.post("/", response_model=ResponseMessage)
def new_company(
        company: NewCompany,
        db = Depends(get_db_connection)
    ):
    try:
        company_id: int = company_database.create_new_company(db, company)
        user_data = NewUser(
            name = company.owner,
            telephone = company.telephone,
            module= [],
            role=[
                Role(
                    id=1,
                    name="Owner"
                )
            ],
            email = company.email,
            type = "owner",
            password = company.password,
            status = True,
        )
        user_id = new_user(db, user_data, company_id)
        for module in company.modules:
            company_module = CompanyModule(
                name=module.name,
                purchase_date=None,
                status="active"
            )
            module_id = add_new_company_module(db, company_module=company_module, company_id=company_id)
            user_module = Module(
                id=module_id,
                name=module.name
            )
            add_user_module(connection=db, module=user_module, user_id=user_id)
        risk_rating(db, company_id)
        engagement_types(db, company_id)
        issue_finding_source(db, company_id)
        control_effectiveness_rating(db, company_id)
        control_weakness_rating(db, company_id)
        audit_opinion_rating(db, company_id)
        risk_maturity_rating(db, company_id)
        issue_implementation_status(db, company_id)
        control_type(db, company_id)
        roles(db, company_id)
        business_process(db, company_id)
        impact_category(db, company_id)
        root_cause_category(db, company_id)
        risk_category(db, company_id)
        return {"detail": "company successfully created", "status_code":201}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=Company)
def get_company(
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = databases.get_companies(db, column="id", value=user.company_id)[0]
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)






