from fastapi import APIRouter, Depends, BackgroundTasks
from Management.users.databases import add_user_module
from utils import get_db_connection
from Management.companies.schemas import *
from Management.company_modules.schemas import CompanyModule
from Management.company_modules.databases import add_new_company_module
from Management.companies import databases as company_database
from Management.users.databases import new_user
from schema import CurrentUser, ResponseMessage
from utils import get_current_user
from Management.companies import databases
from Management.users.schemas import *
from seedings import *
router = APIRouter(prefix="/companies")

@router.post("/", response_model=ResponseMessage)
def new_company(
        company: NewCompany,
        tasks: BackgroundTasks,
        db = Depends(get_db_connection),
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
        tasks.add_task(risk_rating, connection=db, company=company_id)
        tasks.add_task(engagement_types, connection=db, company=company_id)
        tasks.add_task(issue_finding_source, connection=db, company=company_id)
        tasks.add_task(control_effectiveness_rating, connection=db, company=company_id)
        tasks.add_task(control_weakness_rating, connection=db, company=company_id)
        tasks.add_task(audit_opinion_rating, connection=db, company=company_id)
        tasks.add_task(risk_maturity_rating, connection=db, company=company_id)
        tasks.add_task(issue_implementation_status, connection=db, company=company_id)
        tasks.add_task(control_type, connection=db, company=company_id)
        tasks.add_task(roles, connection=db, company=company_id)
        tasks.add_task(business_process, connection=db, company=company_id)
        tasks.add_task(impact_category, connection=db, company=company_id)
        tasks.add_task(root_cause_category, connection=db, company=company_id)
        tasks.add_task(risk_category, connection=db, company=company_id)
        return {"detail": "company successfully created", "status_code":201}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=Company)
def get_company(
        db = Depends(get_db_connection),
        #user: CurrentUser  = Depends(get_current_user)
    ):
    #if user.status_code != 200:
        #raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = databases.get_companies(db, column="id", value=0)[0]
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)






