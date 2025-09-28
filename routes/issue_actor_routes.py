from fastapi import APIRouter, Depends
from models.issue_actor_models import remove_issue_actor_model, get_all_actor_issues_model, \
    get_all_issue_actors_on_issue_model, assign_issue_actor
from schemas.issue_actor_schemas import NewIssueActor
from services.connections.postgres.connections import AsyncDBPoolSingleton
from utils import exception_response, return_checker
from schemas.user_schemas import User
from datetime import datetime



router = APIRouter(prefix="/issue_actors")

@router.post("/{issue_id}")
async def add_issue_actor(
        issue_id: str,
        actor: NewIssueActor,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        user = User(
            id=actor.user_id,
            name=actor.name,
            email=actor.email,
            date_issued=datetime.now()
        )

        results = await assign_issue_actor(
            connection=connection,
            user=user,
            role=actor.role,
            issue_id=issue_id,
            throw=True
        )

        return await return_checker(
            data=results,
            passed="Issue Actor Successfully Added",
            failed="Failed Adding  Issue Actor"
        )



@router.get("/issues/{user_id}")
async def fetch_all_actor_issues(
        user_id: str,
        module_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        data = await get_all_actor_issues_model(
            connection=connection,
            user_id=user_id,
            module_id=module_id
        )

        return data




@router.get("/{issue_id}")
async def fetch_all_issue_actor(
        issue_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():

        data = await get_all_issue_actors_on_issue_model(
            connection=connection,
            issue_id=issue_id
        )

        return data




@router.delete("/{issue_actor_id}")
async def remove_issue_actor(
        issue_actor_id: str,
        connection=Depends(AsyncDBPoolSingleton.get_db_connection),

):
    with exception_response():
        results = await remove_issue_actor_model(
            connection=connection,
            issue_actor_id=issue_actor_id
        )

        return await return_checker(
            data=results,
            passed="Issue Actor Successfully Removed",
            failed="Failed Removing  Issue Actor"
        )

