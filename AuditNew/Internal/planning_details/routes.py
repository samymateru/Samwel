from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.planning_details import databases
from AuditNew.Internal.planning_details.schemas import *
from typing import Tuple, List, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/planning_details")

@router.get("/")
def get_planning_details(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        planning_details_data: List[Dict] = databases.get_planning_details(db)
        if planning_details_data.__len__() == 0:
            return {"message": "no planning details available", "code": 404}
        return planning_details_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_planning_details")
def create_new_planning_detail(
        planning_detail: NewPlanningDetails,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    planning_details_data: Tuple = (
        current_user.company_id,
        planning_detail.task,
        planning_detail.notes,
        planning_detail.status,
        current_user.user_id,
        datetime.now()
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_planning_detail(db, planning_details_data)
        return {"message": "planning details successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_planning_detail")
def update_planning_detail(
        planning_detail: UpdatePlanningDetails,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_planning_detail(db, planning_detail)
        return {"message": "planning detail successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_planning_details")
def delete_planning_details(
        planning_id: DeletePlanningDetails,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_planning_details(db, planning_id.planning_id)
        return {"message": "successfully delete planning detail"}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)