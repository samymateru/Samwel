from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from utils import get_current_user, get_db_connection
from typing import List
from schema import *
from Management.settings.business_process.schemas import *
from Management.settings.business_process.databases import *

router = APIRouter(prefix="/settings")

@router.post("/business_process", response_model=ResponseMessage)
def add_business_process(
        business_process: NewBusinessProcess,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        return {"detail": "Business process added successfully", "status_code": 201}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/business_sub_process", response_model=ResponseMessage)
def add_business_sub_process(
        business_sub_process: NewBusinessProcess,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return {"detail": "Business sub process added successfully", "status_code": 501}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/business_process", response_model=List[BusinessProcess])
def fetch_business_process(
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_business_process(db, column="company", value=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

