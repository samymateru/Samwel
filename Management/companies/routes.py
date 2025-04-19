from fastapi import APIRouter, Depends
from Management.users.databases import add_user_module
from utils import get_async_db_connection
from Management.company_modules.schemas import CompanyModule
from Management.company_modules.databases import add_new_company_module
from Management.users.databases import new_user
from schema import CurrentUser, ResponseMessage
from utils import get_current_user
from background import set_company_profile
from Management.companies.databases import *
from Management.users.schemas import *
import asyncio


router = APIRouter(prefix="/companies")

@router.post("/", response_model=ResponseMessage)
async def create_new_entity(
        company: NewCompany,
        db_async = Depends(get_async_db_connection),
    ):
    try:
        company_id = await create_new_company(connection=db_async, company=company)
        user = NewUser(
            name = company.owner,
            telephone = company.telephone,
            module= [],
            role=[
                Role(
                    name="Owner"
                )
            ],
            email = company.email,
            type = "owner",
            password = company.password,
            status = True,
        )
        user_id = await new_user(connection=db_async, user_=user, company_id=company_id)
        for module in company.modules:
            company_module = CompanyModule(
                name=module.name,
                purchase_date=None,
                status="active"
            )
            module_id = await add_new_company_module(db_async, company_module=company_module, company_id=company_id)
            user_module = Module(
                id=module_id,
                name=module.name
            )
            await add_user_module(connection=db_async, module=user_module, user_id=user_id)
        asyncio.create_task(set_company_profile(company_id=company_id))
        return ResponseMessage(detail="company successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/", response_model=Company)
async def get_company(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_companies(db, company_id=user.company_id)
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)






