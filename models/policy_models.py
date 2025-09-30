from psycopg import AsyncConnection

from core.tables import Tables
from schemas.policy_schemas import NewPolicy, UpdatePolicy, CreatePolicy, PolicyColumns
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key


async def create_new_policy_model(
        connection: AsyncConnection,
        policy: NewPolicy,
        engagement_id: str,
        throw: bool = True
):
    with exception_response():
        __policy__ = CreatePolicy(
            id=get_unique_key(),
            engagement=engagement_id,
            name=policy.name,
            version=policy.version,
            key_areas=policy.key_areas
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.POLICIES.value)
            .values(__policy__)
            .check_exists({PolicyColumns.NAME.value: policy.name})
            .check_exists({PolicyColumns.ENGAGEMENT.value: engagement_id})
            .throw_error_on_exists(throw)
            .returning(PolicyColumns.ID.value)
            .execute()
        )

        return builder



async def get_engagement_policies_model(
        connection: AsyncConnection,
        engagement_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.POLICIES.value)
            .where(PolicyColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder



async def get_single_engagement_policy_model(
        connection: AsyncConnection,
        policy_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.POLICIES.value)
            .where(PolicyColumns.ID.value, policy_id)
            .fetch_one()
        )

        return builder



async def update_engagement_policy_model(
        connection: AsyncConnection,
        policy: UpdatePolicy,
        policy_id: str
):
    with exception_response():
        __policy__ = UpdatePolicy(
            name=policy.name,
            version=policy.version,
            key_areas=policy.key_areas
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.POLICIES.value)
            .values(__policy__)
            .check_exists({PolicyColumns.ID.value: policy_id})
            .where({PolicyColumns.ID.value: policy_id})
            .returning(PolicyColumns.ID.value)
            .execute()
        )

        return builder



async def delete_engagement_policy_model(
        connection: AsyncConnection,
        policy_id: str
):
    with exception_response():

        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.POLICIES.value)
            .check_exists({PolicyColumns.ID.value: policy_id})
            .where({PolicyColumns.ID.value: policy_id})
            .returning(PolicyColumns.ID.value)
            .execute()
        )

        return builder
