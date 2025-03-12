from fastapi import APIRouter, Depends, HTTPException
from schema import CurrentUser
from utils import get_current_user, get_db_connection
from typing import List
from schema import *
from Management.companies.profile.impact_category.schemas import *
from Management.companies.profile.impact_category.databases import *

router = APIRouter(prefix="/profile")

@router.post("/impact_category/{company_id}", response_model=ResponseMessage)
def create_new_impact_category(
        company_id: int,
        impact_category: NewImpactCategory,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        return {"detail": "Business process added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/impact_sub_category/{impact_category_id}", response_model=ResponseMessage)
def create_new_impact_sub_category(
        impact_category_id: int,
        impact_sub_category: NewImpactSubCategory,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:

        return {"detail": "Business sub process added successfully"}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/impact_category/{company_id}", response_model=List[NewImpactCategory])
def fetch_impact_category(
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

@router.get("/impact_sub_category/{impact_category_id}", response_model=List[NewImpactSubCategory])
def fetch_impact_sub_category(
        impact_category_id: int,
        db = Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/impact_category/{impact_category_id}")
def update_impact_category(
        impact_category_id: int,
        impact_category: NewImpactCategory,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/impact_sub_category/{impact_sub_category_id}")
def update_impact_sub_category(
        impact_sub_category_id: int,
        impact_sub_category: NewImpactSubCategory,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/impact_category/{impact_category_id}")
def delete_business_process(
        impact_category_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/impact_sub_category/{impact_sub_category_id}")
def delete_impact_sub_category(
        impact_sub_category_id: int,
        db=Depends(get_db_connection),
        user: CurrentUser = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
       pass
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

