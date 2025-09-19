from fastapi import APIRouter, Depends
from utils import get_async_db_connection
from AuditNew.Internal.engagements.databases import *
from typing import List
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from datetime import datetime
import asyncio
from background import set_engagement_templates

router = APIRouter(prefix="/engagements")

@router.get("/{annual_id}", response_model=List[Engagement])
async def fetch_engagements(
        annual_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_engagements(connection=db, annual_id=annual_id, email=user.user_email)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/{annual_id}", response_model=ResponseMessage)
async def create_new_engagement(
        annual_id: str,
        engagement: Engagement,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    max_ = 0
    try:
        code_list = await get_engagement_code(connection=db, annual_id=annual_id)
        for data in code_list:
            code = data[0].split("-")
            if engagement.department.code == code[0]:
                if int(code[1]) >= max_:
                    max_ = int(code[1])
        engagement_code: str = engagement.department.code + "-" + str(max_ + 1).zfill(3) + "-" + str(datetime.now().year)
        engagement_id = await add_new_engagement(
            connection=db,
            engagement=engagement,
            plan_id=annual_id,
            code=engagement_code,
            module_id=user.module_id
        )
        asyncio.create_task(set_engagement_templates(engagement_id=engagement_id))
        return ResponseMessage(detail="Engagement successfully created")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/{engagement_id}", response_model=ResponseMessage)
async def update_engagement(
        engagement_id: str,
        engagement: UpdateEngagement,
        db = Depends(get_async_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        return HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await edit_engagement(connection=db, engagement=engagement, engagement_id=engagement_id)
        return ResponseMessage(detail="Engagement successfully updated")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

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



@router.get("/completed/{module_id}", response_model=List[Engagement])
async def fetch_completed_engagements(
        module_id: str,
        db = Depends(get_async_db_connection),
        #user: CurrentUser  = Depends(get_current_user)
):
    with exception_response():
        data = await get_completed_engagement(connection=db, module_id=module_id)
        return data


@router.put("/complete/{engagement_id}", response_model=ResponseMessage)
async def mark_engagement_as_complete(
        engagement_id: str,
        db = Depends(get_async_db_connection),
        #user: CurrentUser  = Depends(get_current_user)
):
    with exception_response():
        data = await complete_engagement(connection=db, engagement_id=engagement_id)
        if data is None:
            raise HTTPException(status_code=400, detail="Unknown Engagement")
        return ResponseMessage(detail="Engagement Successfully Completed")