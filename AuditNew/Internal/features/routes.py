from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.features import databases
from AuditNew.Internal.features.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/features")

@router.get("/")
def get_features(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        feature_data: List[Dict] = databases.get_features(db)
        if feature_data.__len__() == 0:
            return {"message": "no features available", "code": 404}
        return feature_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_feature")
def create_new_feature(
        feature: NewFeature,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    new_feature_data: Tuple = (
        feature.module_id,
        feature.name,
        feature.description,
        feature.is_active,
        datetime.now(),
        datetime.now()
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_feature(db, new_feature_data)
        return {"message": "feature successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_feature")
def update_feature(
        feature: UpdateFeature,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_feature(db, feature)
        return {"message": "feature successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_features")
def delete_features(
        feature_id: DeleteFeature,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_features(db, feature_id.feature_id)
        return {"message": "successfully delete the features", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)