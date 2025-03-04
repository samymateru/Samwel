from fastapi import APIRouter, Depends, HTTPException, Query
from utils import get_db_connection
from Management.companies.schemas import *
from typing import Tuple, List, Dict
from Management.companies import databases as company_database
from Management.users import databases as user_database
from schema import CurrentUser
from utils import generate_hash_password, get_current_user
from Management.companies import databases
from Management.users.schemas import *
from seedings import *
router = APIRouter(prefix="/companies")

@router.post("/new_company")
def new_company(
        new_company_data: NewCompany,
        db = Depends(get_db_connection)
    ):
    try:
        company_id: int = company_database.create_new_company(db, new_company_data)
        user_data = NewUser(
            name = new_company_data.owner,
            telephone = new_company_data.telephone,
            module= [""],
            role=Role(
                id = 1,
                name = "Owner"
            ),
            email = new_company_data.email,
            type = "owner",
            password = new_company_data.password,
            status = True,
        )
        user_database.new_user(db, user_data, company_id)
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
        return {"detail": "company successfully created", "status_code":201}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/")
def get_company(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        company_data: List[Dict] = databases.get_companies(db, column="id", value=current_user.company_id)
        if company_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": company_data[0], "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)






