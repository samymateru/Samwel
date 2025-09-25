from fastapi import APIRouter, Depends
from schema import ResponseMessage
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response


router = APIRouter(prefix="/")

@router.get("/entity/{entity_id}", response_model=ResponseMessage)
async def fetch_entity_users(
        entity_id: Optional[str] = None,
        connection = Depends(AsyncDBPoolSingleton.get_db_connection),
):
    with exception_response():
        pass
