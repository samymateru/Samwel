from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.users import databases
from Management.users.schemas import *
from typing import Dict
from utils import get_current_user
from schema import CurrentUser
from Management.roles.databases import get_roles


router = APIRouter(prefix="/users")

@router.get("/")
def get_users(
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        user_data: List[Dict] = databases.get_user(db, row=list(User.model_fields.keys()), column="company_id", value=current_user.company_id)
        if user_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": user_data, "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/profile/{user_id}")
def get_users(
        user_id: int,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        user_data: List[Dict] = databases.get_user(db, row=list(User.model_fields.keys()), column="id", value=user_id)
        if user_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": user_data, "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/new_user")
def create_new_user(
        user: NewUser,
        db = Depends(get_db_connection),
        current_user: CurrentUser  = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        databases.create_new_user(connection=db, user_data=user,  company_id=current_user.company_id)
        return {"detail": "user successfully created", "status_code": 501}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/update_user")
def update_user(
        user_update: UpdateUser,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        databases.update_user(db, user_update)
        return {"detail": "user successfully updated", "status_code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/delete_user")
def delete_user(
        users_id: DeleteUser,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        user_type: str = databases.get_user(db, column="id", value=users_id.id, row=["type"])[0].get("type")
        if user_type == "user":
            databases.delete_user(db, users_id.id)
            return {"detail": "successfully delete the user", "status_code": 503}
        else:
            return HTTPException(status_code=101, detail="This user cant be deleted")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/add_role")
def create_new_role(
        role: AddRole,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        databases.add_role(db, user_id=role.user_id, role_id=role.role_id)
        return {"detail": "role added successfully", "status_code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/remove_role")
def remove_role(
        role: AddRole,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
):
    print(role)
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="Your not admin")
    try:
        databases.remove_role(db, role_id=role.role_id, user_id=role.user_id)
        return {"detail": "role remove successfully", "status_code": 503}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)