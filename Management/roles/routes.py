from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.roles import databases
from Management.users import databases as user_database
from Management.roles.schemas import *
from typing import Tuple, Dict
from utils import get_current_user
from schema import CurrentUser
from datetime import datetime
from Management.users.databases import add_role

router = APIRouter(prefix="/roles")

@router.get("/modules")
def get_module_roles(
        db = Depends(get_db_connection),
        # current_user: CurrentUser = Depends(get_current_user)
):
    # if current_user.status_code != 200:
    #     return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    try:
        roles_data: List[Dict] = databases.fetch_module_roles(db)
        if roles_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": roles_data, "status_code": 200}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get("/")
# def get_company_roles(
#         db = Depends(get_db_connection),
#         current_user: CurrentUser = Depends(get_current_user)
# ):
#     if current_user.status_code != 200:
#         return HTTPException(status_code=current_user.status_code, detail=current_user.description)
#     if current_user.type != "admin":
#         return HTTPException(status_code=101, detail="Your not admin")
#     try:
#         roles_data: List[Dict] = databases.get_roles(db, column="company_id", value=current_user.company_id)
#         if roles_data.__len__() == 0:
#             return {"detail": "no roles available", "status_code": 201}
#         return {"payload": roles_data, "status_code": 200}
#     except HTTPException as e:
#         return HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.get("/{user_id}")
# def get_user_roles(
#         user_id: int,
#         db = Depends(get_db_connection),
#         current_user: CurrentUser = Depends(get_current_user)
# ):
#     if current_user.status_code != 200:
#         return HTTPException(status_code=current_user.status_code, detail=current_user.description)
#     if current_user.type != "admin":
#         return HTTPException(status_code=101, detail="Your not admin")
#     try:
#         role_ids: List[int] = user_database.get_user(db, column="id", value=user_id)[0].get("role_id")
#         user_roles = databases.get_user_roles(db, role_ids)
#         return {"payload": user_roles, "status_code": 200}
#     except HTTPException as e:
#         return HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.post("/new_role")
# def create_new_role(
#         role: NewRole,
#         db = Depends(get_db_connection),
#         current_user: CurrentUser = Depends(get_current_user)
# ):
#     if current_user.status_code != 200:
#         return HTTPException(status_code=current_user.status_code, detail=current_user.description)
#     if current_user.type != "admin":
#         return HTTPException(status_code=101, detail="Your not admin")
#     try:
#         databases.create_new_role(db, role, str(current_user.company_id))
#         return {"detail": "role successfully created", "status_code": 501}
#     except HTTPException as e:
#         return HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.put("/update_role")
# def update_role(
#         role_update: UpdateRole,
#         db = Depends(get_db_connection),
#         current_user: CurrentUser = Depends(get_current_user)
# ):
#     if current_user.status_code != 200:
#         return HTTPException(status_code=current_user.status_code, detail=current_user.description)
#     if current_user.type != "admin":
#         return HTTPException(status_code=101, detail="Your not admin")
#     try:
#         databases.update_role(db, role_update)
#         return {"message": "roles successfully updated", "code": 502}
#     except HTTPException as e:
#         return HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.delete("/delete_role")
# def delete(
#         roles_id: DeleteRoles,
#         db = Depends(get_db_connection),
#         current_user: CurrentUser = Depends(get_current_user)
# ):
#     if current_user.status_code != 200:
#         return HTTPException(status_code=current_user.status_code, detail=current_user.description)
#     if current_user.type != "admin":
#         return HTTPException(status_code=101, detail="Your not admin")
#     try:
#         databases.delete_role(db, roles_id.roles_id)
#         return {"message": "successfully delete the role", "code": 503}
#     except HTTPException as e:
#         return HTTPException(status_code=e.status_code, detail=e.detail)
