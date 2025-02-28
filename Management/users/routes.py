from fastapi import APIRouter, Depends, HTTPException
from utils import  get_db_connection
from Management.users.databases import *
from Management.users.schemas import *
from utils import get_current_user
from schema import CurrentUser
from Management.roles.databases import *


router = APIRouter(prefix="/users")

@router.get("/")
def fetch_users(
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        user_data = get_user(db, column="company", value=user.company_id)
        if user_data.__len__() == 0:
            return {"payload": [], "status_code": 200}
        return {"payload": user_data, "status_code": 200}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{user_id}", response_model=User)
def fetch_user(
        user_id: int,
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = get_user(db, column="id", value=user_id)[0]
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/")
def create_new_user(
        user_data: NewUser,
        db = Depends(get_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        new_user(connection=db, user_data=user_data,  company_id=user.company_id)
        return {"detail": "user successfully created", "status_code": 501}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.put("/")
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
        update_user(db, user_update)
        return {"detail": "user successfully updated", "status_code": 502}
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)

@router.delete("/")
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
        user_type: str = get_user(db, column="id", value=users_id.id, row=["type"])[0].get("type")
        if user_type == "user":
            delete_user(db, users_id.id)
            return {"detail": "successfully delete the user", "status_code": 503}
        else:
            return HTTPException(status_code=101, detail="This user cant be deleted")
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)



