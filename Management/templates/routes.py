from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.templates.databases import *
from Management.templates.schemas import *
from schema import CurrentUser
from utils import get_current_user

router = APIRouter(prefix="/templates")
@router.get("/")
def get_templates(
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        template_data: List[Dict] = get_template(db, company_id=str(current_user.company_id))
        if template_data.__len__() == 0:
            return {"detail": "no templates available", "status_code": 201}
        return {"payload": template_data, "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_template")
def create_new_template(
        template: NewTemplate,
        db=Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        create_engagement_template(db, template, str(current_user.company_id))
        return {"detail": "template successfully created", "status_code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)