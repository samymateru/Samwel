from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.staff_assignment import databases
from AuditNew.Internal.staff_assignment.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/staff_assignment")

@router.get("/")
def get_staff_assignments(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        staff_assignment_data: List[Dict] = databases.get_staff_assignment(db)
        if staff_assignment_data.__len__() == 0:
            return {"message": "no staff assignment", "code": 404}
        return staff_assignment_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_staff_assignment")
def create_new_staff_assignment(
        staff_assignment: NewStaffAssignment,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    new_staff_assignment_data: Tuple = (
        staff_assignment.engagement_id,
        current_user.user_id,
        staff_assignment.role
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_staff_assignment(db, new_staff_assignment_data)
        return {"message": "staff assignment successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_staff_assignment")
def update_staff_assignment(
        staff_assignment: UpdateStaffAssignment,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_staff_assignment(db, staff_assignment)
        return {"message": "staff assignment successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_staff_assignment")
def delete_staff_assignment(
        assignment_id: DeleteStaffAssignment,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_staff_assignment(db, assignment_id.assignment_id)
        return {"message": "successfully delete the staff assignment", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
