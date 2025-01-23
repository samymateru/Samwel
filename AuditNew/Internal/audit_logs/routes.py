from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.audit_logs import databases
from AuditNew.Internal.audit_logs.schemas import *
from typing import Tuple, List, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/audit_logs")

@router.get("/")
def get_audit_logs(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        audit_log_data: List[Dict] = databases.get_audit_logs(db)
        if len(audit_log_data) == 0:
            return {"message": "no audit logs available", "code": 404}
        return audit_log_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)


@router.post("/new_annual_plan")
def create_new_audit_log(
        audit_log: NewAuditLog,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    new_audit_log: Tuple = (
        current_user.user_id,
        audit_log.action,
        audit_log.description,
        datetime.now(),
        datetime.now()
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_audit_log(db, new_audit_log)
        return {"message": "audit log successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/update_audit_log")
def update_audit_log(
        audit_log: UpdateAuditLog,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_audit_log(db, audit_log)
        return {"message": "audit log successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_audit_log")
def delete_audit_log(
        log_id: DeleteAuditLogs,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_audit_log(db, log_id.log_id)
        return {"message": "successfully delete the annual plan", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
