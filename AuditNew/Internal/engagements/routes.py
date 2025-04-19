from fastapi import APIRouter, Depends
from AuditNew.Internal.engagements.administration.databases import add_new_business_contact
from utils import get_async_db_connection
from AuditNew.Internal.engagements.databases import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from datetime import datetime
from seedings import planning_procedures, finalization_procedures, reporting_procedures, add_engagement_profile


router = APIRouter(prefix="/engagements")

@router.get("/{annual_id}", response_model=List[Engagement])
async def fetch_engagements(
        annual_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        return HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagements(connection=db, annual_id=annual_id)
        return data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{annual_id}", response_model=ResponseMessage)
async def create_new_engagement(
        annual_id: str,
        engagement: Engagement,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    eng: str | int = await get_engagement_code(connection=db, annual_id=annual_id)
    if user.status_code != 200:
        return HTTPException(status_code=user.status_code, detail=user.description)
    max_ = 0
    try:
        for data in eng:
            if engagement.department.code == data[0].split("-")[0]:
                if int(data[0].split("-")[1]) >= max_:
                    max_ = int(data[0].split("-")[1])
        code: str = engagement.department.code + "-" + str(max_ + 1).zfill(3) + "-" + str(datetime.now().year)
        id = await create_new_engagement(
            connection=db,
            engagement=engagement,
            annual_id=annual_id,
            code=code)
        await planning_procedures(connection=db, engagement=id)
        await finalization_procedures(connection=db, engagement=id)
        await reporting_procedures(connection=db, engagement=id)
        await add_engagement_profile(connection=db, engagement=id)
        await add_new_business_contact(connection=db, engagement_id=id)
        return ResponseMessage(detail="Engagement successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_engagement/{engagement_id}", response_model=ResponseMessage)
async def update_engagement(
        engagement_id: str,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:

        return ResponseMessage(detail="Engagement successfully updated")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/{engagement_id}")
async def delete_engagement(
        engagement_id: str,
        db = Depends(get_async_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        await delete_engagement(connection=db, engagement_id=engagement_id)
        return ResponseMessage(detail="Engagement successfully deleted")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
