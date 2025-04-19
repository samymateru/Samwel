from fastapi import APIRouter, Depends, HTTPException
from utils import get_db_connection, get_async_db_connection
from Management.users.databases import *
from Management.users.schemas import *
from utils import get_current_user
from schema import CurrentUser, ResponseMessage
from Management.roles.databases import *


router = APIRouter(prefix="/users")

@router.get("/", response_model=List[User])
async def fetch_users(
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_users(db, company_id=user.company_id)
        return data
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/{user_id}", response_model=User)
async def fetch_user(
        user_id: str,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        data = await get_user(connection=db, user_id=user_id)
        if data.__len__() == 0:
            raise HTTPException(status_code=400, detail="User not found")
        return data[0]
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/", response_model=ResponseMessage)
async def create_new_user(
        user_: NewUser,
        db = Depends(get_async_db_connection),
        user: CurrentUser  = Depends(get_current_user)
    ):
    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code, detail=user.description)
    try:
        await new_user(connection=db, user_=user_,  company_id=user.company_id)
        return ResponseMessage(detail="User successfully created")
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

@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db = Depends(get_db_connection),
        current_user: CurrentUser = Depends(get_current_user)
    ):
    if current_user.status_code != 200:
        return HTTPException(status_code=current_user.status_code, detail=current_user.description)
    if current_user.type != "admin":
        return HTTPException(status_code=101, detail="your not admin")
    try:
        pass
    except HTTPException as e:
        return HTTPException(status_code=e.status_code, detail=e.detail)



