from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from utils import get_current_user, get_db_connection
from typing import List
from schema import *
from Management.companies.profile.business_process.schemas import *
from Management.companies.profile.business_process.databases import *

router = APIRouter(prefix="/profile")

@router.post("/business_process/{company_id}", response_model=ResponseMessage)
def create_new_business_process(
        company_id: int,
        business_process: NewBusinessProcess,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        return {"detail": "Business process added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/business_sub_process/{business_process_id}", response_model=ResponseMessage)
def create_new_business_sub_process(
        business_process_id: int,
        business_sub_process: NewBusinessProcess,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return {"detail": "Business sub process added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{company_id}", response_model=List[BusinessProcess])
def fetch_business_process(
        company_id: int,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{business_process_id}", response_model=List[BusinessProcess])
def fetch_business_sub_process(
        business_process_id: int,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/business_process/{business_process_id}")
def update_business_process():
    pass