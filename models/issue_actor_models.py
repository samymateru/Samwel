from psycopg import AsyncConnection
from core.tables import Tables
from schemas.issue_actor_schemas import CreateIssueActor, IssueActors, IssueActorColumns
from schemas.user_schemas import User
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def assign_issue_actor(
        connection: AsyncConnection,
        user: User,
        role: IssueActors,
        issue_id: str
):
    with exception_response():
        __user__ = CreateIssueActor(
            issue_actor_id=get_unique_key(),
            user_id=user.id,
            name=user.name,
            email=user.email,
            role=role.value,
            issue_id=issue_id,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ISSUE_ACTORS.value)
            .values(__user__)
            .check_exists({IssueActorColumns.ISSUE_ID.value: issue_id})
            .check_exists({IssueActorColumns.USER_ID.value: user.id})
            .throw_error_on_exists(False)
            .returning(IssueActorColumns.ISSUE_ACTOR_ID.value)
            .execute()
        )
        return builder


async def get_all_issue_actors_on_issue_model(
        connection: AsyncConnection,
        issue_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value)
            .where(IssueActorColumns.ISSUE_ID.value, issue_id)
            .fetch_all()
        )

        return builder


async def get_issue_actors_on_issue_based_on_role_model(
        connection: AsyncConnection,
        issue_id: str,
        role: IssueActors
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value)
            .where(IssueActorColumns.ISSUE_ID.value, issue_id)
            .where(IssueActorColumns.ROLE.value, role.value)
            .fetch_all()
        )

        return builder


async def remove_issue_actor_model(
        connection: AsyncConnection,
        issue_id: str,
        user_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value)
            .check_exists({
                IssueActorColumns.ISSUE_ID.value: issue_id,
                IssueActorColumns.USER_ID.value: user_id
            })
            .where({
                IssueActorColumns.ISSUE_ID.value: issue_id,
                IssueActorColumns.USER_ID.value: user_id
            })
            .returning(IssueActorColumns.ISSUE_ACTOR_ID.value)
            .execute()
        )

        return builder