from typing import List

from fastapi import HTTPException
from psycopg import AsyncConnection
from core.tables import Tables
from schemas.issue_actor_schemas import CreateIssueActor, IssueActors, IssueActorColumns
from schemas.issue_schemas import NewIssue, IssueColumns
from schemas.user_schemas import User, ModuleUserColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from utils import exception_response, get_unique_key
from datetime import datetime



async def assign_issue_actor(
        connection: AsyncConnection,
        user: User,
        role: IssueActors,
        issue_id: str,
        throw: bool = False
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
            .check_exists({IssueActorColumns.ROLE.value: role.value})
            .check_exists({IssueActorColumns.USER_ID.value: user.id})
            .check_exists({IssueActorColumns.ISSUE_ID.value: issue_id})
            .throw_error_on_exists(throw)
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


async def get_all_issue_actors_on_issue_by_status_model(
        connection: AsyncConnection,
        issue_id: str,
        roles=None
):
    if roles is None:
        roles = ["lod2_risk_manager", "lod2_compliance_officer"]

    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value, alias="iss_act")
            .join(
                "LEFT",
                Tables.MODULES_USERS.value,
                "mod_usr.user_id = iss_act.user_id",
                "mod_usr",
                use_prefix=False
            )
            .where("iss_act."+IssueActorColumns.ISSUE_ID.value, issue_id)
            .where("iss_act."+IssueActorColumns.ROLE.value, roles)
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
        issue_actor_id: str,
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value)
            .check_exists({IssueActorColumns.ISSUE_ACTOR_ID.value: issue_actor_id})
            .where({IssueActorColumns.ISSUE_ACTOR_ID.value: issue_actor_id})
            .returning(IssueActorColumns.ISSUE_ACTOR_ID.value)
            .execute()
        )

        return builder



async def initialize_issue_actors(
        connection: AsyncConnection,
        issue_id: str,
        issue: NewIssue,
):
    with exception_response():

        for user in issue.lod1_owner:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.OWNER,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        for user in issue.lod1_implementer:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.IMPLEMENTER,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        for user in issue.lod2_risk_manager:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.RISK_MANAGER,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        for user in issue.lod2_compliance_officer:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.COMPLIANCE_OFFICER,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        for user in issue.lod3_audit_manager:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.AUDIT_MANAGER,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        for user in issue.observers:
            result = await assign_issue_actor(
                connection=connection,
                user=User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    date_issued=datetime.now()
                ),
                role=IssueActors.OBSERVERS,
                issue_id=issue_id
            )
            if result is None:
                raise HTTPException(status_code=400, detail="Error While Assign Issue Actors")

        return True



async def get_all_actor_issues_model(
        connection: AsyncConnection,
        user_id: str,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ISSUE_ACTORS.value, alias="iss_act")
            .join(
                "LEFT",
                Tables.ISSUES.value,
                "iss.id = iss_act.issue_id",
                "iss",
                use_prefix=False
            )
            .where("iss_act."+IssueActorColumns.USER_ID.value, user_id)
            .where("iss."+IssueColumns.MODULE_ID.value, module_id)
            .fetch_all()
        )

        return builder

