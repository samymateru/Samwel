from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from AuditNew.Internal.feature_records import databases
from AuditNew.Internal.feature_records.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime

router = APIRouter(prefix="/feature_records")

@router.get("/")
def get_feature_records(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        feature_record_data: List[Dict] = databases.get_feature_records(db)
        if feature_record_data.__len__() == 0:
            return {"message": "no feature record available", "code": 404}
        return feature_record_data
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_feature_record")
def create_new_feature_record(
        feature_record: NewFeatureRecord,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    feature_record_data: Tuple = (
        feature_record.feature_id,
        feature_record.title,
        feature_record.record_type,
        feature_record.data,
        current_user.user_id,
        current_user.user_id,
        datetime.now(),
        datetime.now()
    )
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.create_new_feature_record(db, feature_record_data)
        return {"message": "feature record successfully created", "code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.put("/update_feature_record")
def update_feature_record(
        feature_record: UpdateFeatureRecord,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.update_feature_record(db, feature_record)
        return {"message": "feature record successfully updated", "code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_feature_record")
def delete_feature_record(
        record_id: DeleteFeatureRecord,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        databases.delete_feature_record(db, record_id.record_id)
        return {"message": "successfully delete the feature record", "code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)
