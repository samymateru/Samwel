from typing import Union
from psycopg import AsyncConnection
from core.tables import Tables
from schemas.annual_plan_schemas import ReadAnnualPlan
from schemas.engagement_schemas import  JoinEngagementTest
from schemas.role_schemas import CreateRole, RoleColumns, UpdateRole
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response


async def create_role_model(
        connection: AsyncConnection,
        role: Union[CreateRole, list[CreateRole]]
):
    with exception_response():
        """
        Creates a new role in the database.

        Ensures the role name is unique within the same module before inserting.
        Returns the inserted role details or raises an error if it already exists.
        """
        with exception_response():
            builder = InsertQueryBuilder(connection=connection).into_table(Tables.ROLES.value).values(role)

            # handle check_exists for single or multiple
            if isinstance(role, list):
                # For multiple roles, you may skip the check_exists or handle per role before insertion
                pass  # optional: implement batch existence check
            else:
                builder.check_exists({
                    RoleColumns.NAME.value: role.name,
                    RoleColumns.MODULE.value: role.module,
                })

            builder.returning(RoleColumns.NAME.value)

            return await builder.execute()


async def get_module_roles_model(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ROLES.value)
            .where(RoleColumns.MODULE.value, module_id)
            .fetch_all()
        )

        return builder


async def get_role_data_model(
        connection: AsyncConnection,
        role_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ROLES.value)
            .where(RoleColumns.ID.value, role_id)
            .fetch_one()
        )

        return builder



async def get_user_role_model(
        connection: AsyncConnection,
        role_name: str,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ROLES.value)
            .where(RoleColumns.NAME.value, role_name)
            .where(RoleColumns.MODULE.value, module_id)
            .fetch_one()
        )

        return builder



async def update_role_model(
        connection: AsyncConnection,
        role: UpdateRole,
        role_id: str
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ROLES.value)
            .values(role)
            .check_exists({RoleColumns.ID.value: role_id})
            .where({RoleColumns.ID.value: role_id})
            .returning(RoleColumns.ID.value)
            .execute()
        )

        return builder



async def delete_role_model(
        connection: AsyncConnection,
        role_id: str
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.ROLES.value)
            .check_exists({RoleColumns.ID.value: role_id})
            .where({RoleColumns.ID.value: role_id})
            .returning(RoleColumns.ID.value)
            .execute()
        )

        return builder




async def generate_role_reference_model(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        pass




async def generate_role_reference_model_(
        connection: AsyncConnection,
        module_id: str
):
    builder =   await (
        ReadBuilder(connection=connection)
        .from_table("annual_plans", alias="ap")
        .select(ReadAnnualPlan)
        .join_aggregate(
            table="engagements",
            alias="eng",
            on="ap.id = eng.plan_id",
            aggregate_column="id",
            json_field_name="engagements",
            model=JoinEngagementTest,
            use_prefix=True,
            filter_condition={
                "eng.status__in": ['Pending', 'Deleted'],
            },
            order_by="eng.created_at ASC",
            limit=3
        )

        .where("eng.plan_id", module_id)
        .select_joins()
        .fetch_all()
    )

    return  builder
