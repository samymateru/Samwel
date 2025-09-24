from fastapi import APIRouter, Depends, Query
from schemas.issue_schemas import NewIssue
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response

router = APIRouter(prefix="/work_program")

@router.post("/{engagement_id}")
async def create_new_work_program(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.get("/{engagement_id}")
async def fetch_all_work_programs(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.put("/{work_program_id}")
async def update_work_programs(
        work_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass


@router.delete("/{work_program_id}")
async def remove_work_programs(
        work_program_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass



@router.get("/{engagement_id}")
async def fetch_work_program_combined(
        engagement_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass

