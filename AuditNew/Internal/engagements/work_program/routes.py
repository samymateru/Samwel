from fastapi import APIRouter, Depends, UploadFile, File, Query
from utils import  get_async_db_connection
from AuditNew.Internal.engagements.work_program.databases import *
from AuditNew.Internal.engagements.work_program.schemas import *
from utils import get_current_user
from schema import CurrentUser
from schema import ResponseMessage

router = APIRouter(prefix="/engagements")

# @router.post("/main_program/{engagement_id}", response_model=ResponseMessage)
# async def create_new_main_program(
#         engagement_id: str,
#         program: MainProgram,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await add_new_main_program(db, program=program, engagement_id=engagement_id)
#         return ResponseMessage(detail="Program added successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get("/main_program/{engagement_id}", response_model=List[MainProgram])
# async def fetch_main_program(
#         engagement_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_main_program(connection=db, engagement_id=engagement_id)
#         return data
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.put("/main_program/{program_id}", response_model=ResponseMessage)
# async def update_main_program(
#         program_id: str,
#         program: MainProgram,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await edit_main_program(db, program=program, program_id=program_id)
#         return ResponseMessage(detail="Program successfully updated")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get("/work_program/{engagement_id}", response_model=List[WorkProgram])
# async def fetch_work_program(
#         engagement_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_work_program(db, engagement_id=engagement_id)
#         return data
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.delete("/main_program/{program_id}", response_model=ResponseMessage)
# async def delete_main_program(
#         program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await remove_work_program(connection=db, id=program_id, table="main_program", resource="Main program")
#         return ResponseMessage(detail="Program deleted successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

#
# @router.post("/sub_program/{program_id}", response_model=ResponseMessage)
# async def create_new_sub_program(
#         program_id: str,
#         sub_program: NewSubProgram,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await add_new_sub_program(db, sub_program=sub_program, program_id=program_id)
#         return ResponseMessage(detail="Procedure added successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get("/sub_program/{program_id}", response_model=List[SubProgram])
# async def fetch_sub_programs(
#         program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_sub_program(db, program_id=program_id)
#         return data
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.get("/sub_program_/{sub_program_id}", response_model=SubProgram | None)
# async def fetch_sub_program(
#         sub_program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_sub_program_(db, sub_program_id=sub_program_id)
#         if data.__len__() == 0:
#             return None
#         return data[0]
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.put("/sub_program/{sub_program_id}", response_model=ResponseMessage)
# async def update_sub_program(
#         sub_program_id: str,
#         sub_program: SubProgram,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await edit_sub_program(db, sub_program=sub_program, sub_program_id=sub_program_id)
#         return ResponseMessage(detail="Sub program successfully updated")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)

# @router.delete("/sub_program/{sub_program_id}", response_model=ResponseMessage)
# async def delete_sub_program(
#         sub_program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await remove_work_program(connection=db, id=sub_program_id, table="sub_program", resource="Sub program")
#         return ResponseMessage(detail="Sub program deleted successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)


# @router.post("/sub_program/risk_control/{sub_program_id}", response_model=ResponseMessage)
# async def create_new_sub_program_risk_control(
#         sub_program_id: str,
#         risk_control: RiskControl,
#         engagement_id: str = Query(...),
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await add_new_sub_program_risk_control(
#             connection=db,
#             risk_control=risk_control,
#             sub_program_id=sub_program_id,
#             engagement_id=engagement_id
#         )
#         return {"detail": "Risk added successfully"}
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.get("/sub_program/risk_control/{sub_program_id}", response_model=List[RiskControl])
# async def fetch_sub_program_risk_control(
#         sub_program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_sub_program_risk_control(db, sub_program_id=sub_program_id)
#         return data
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)



# @router.get("/sub_program/evidence/{sub_program_id}", response_model=List[SubProgramEvidence])
# async def fetch_engagement_letter(
#         sub_program_id: str,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         data = await get_sub_program_evidence(db, sub_program_id=sub_program_id)
#         return data
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)


# #######################################################################################
# @router.put("/sub_program/save/{sub_program_id}", response_model=ResponseMessage)
# async def save_sub_program(
#         sub_program_id: str,
#         sub_program: SaveWorkProgramProcedure,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await save_sub_program_(db, sub_program=sub_program, sub_program_id=sub_program_id)
#         return ResponseMessage(detail="Sub program saved successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.put("/sub_program/prepare/{sub_program_id}", response_model=ResponseMessage)
# async def edit_prepared_by(
#         sub_program_id: str,
#         sub_program: PreparedReviewedBy,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await edit_work_program_procedure_prepared(db, sub_program=sub_program, sub_program_id=sub_program_id)
#         return ResponseMessage(detail="Sub program prepared successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)
#
# @router.put("/sub_program/review/{sub_program_id}", response_model=ResponseMessage)
# async def edit_reviewed_by(
#         sub_program_id: str,
#         sub_program: PreparedReviewedBy,
#         db=Depends(get_async_db_connection),
#         user: CurrentUser = Depends(get_current_user)
# ):
#     if user.status_code != 200:
#         raise HTTPException(status_code=user.status_code, detail=user.description)
#     try:
#         await edit_work_program_procedure_reviewed(db, sub_program=sub_program, sub_program_id=sub_program_id)
#         return ResponseMessage(detail="Sub program prepared successfully")
#     except HTTPException as e:
#         raise HTTPException(status_code=e.status_code, detail=e.detail)















