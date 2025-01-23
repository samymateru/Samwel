from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagements import databases
from AuditNew.Internal.engagements.schemas import *
from typing import Dict, List
from utils import get_current_user
from schema import CurrentUser


router = APIRouter(prefix="/engagements")

@router.get("/{annual_id}")
def get_engagements(
        annual_id: str,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        engagement_data: List[Dict] = databases.get_engagements(db, row=list(Engagement.model_fields.keys()), column="annual_plan_id", value=annual_id)
        if engagement_data.__len__() == 0:
            return {"detail": "no engagement available", "status_code": 100}
        return {"payload": engagement_data, "status_code":200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_engagement/{annual_id}")
def create_new_engagement(
        annual_id: str,
        engagement: NewEngagement,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    print(annual_id)
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_engagement(db, engagement, annual_id)
        return {"detail": "engagement successfully created", "status_code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_engagement")
def update_engagement(
        user_update: UpdateEngagement,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_engagement(db, user_update)
        return {"message": "engagement successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_engagement")
def delete_engagement(
        engagement_id: DeleteEngagements,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_engagements(db, engagement_id.engagement_id)
        return {"message": "successfully delete the engagement", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
