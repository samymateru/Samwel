from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.engagement_profile import databases
from AuditNew.Internal.engagement_profile.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser

router = APIRouter(prefix="/engagement_profile")

@router.get("/")
def get_engagement_profile(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        engagement_profile_data: List[Dict] = databases.get_engagement_profile(db)
        if engagement_profile_data.__len__() == 0:
            return {"message": "no engagement profile available", "code": 404}
        return engagement_profile_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_engagement_profile")
def create_new_engagement_profile(
        engagement_profile: NewEngagementProfile,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    new_engagement_profile_data: Tuple = (
        engagement_profile.engagement_id,
        engagement_profile.profile_name,
        engagement_profile.key_contacts,
        engagement_profile.estimated_time,
        engagement_profile.business_context
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_engagement_profile(db, new_engagement_profile_data)
        return {"message": "engagement profile successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_engagement_profile")
def update_engagement_profile(
        user_update: UpdateEngagementProfile,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_engagement_profile(db, user_update)
        return {"message": "engagement successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_engagement_profile")
def delete_engagement_profile(
        profile_id: DeleteEngagementProfile,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_engagement_profile(db, profile_id.profile_id)
        return {"message": "successfully delete the engagement profile", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
