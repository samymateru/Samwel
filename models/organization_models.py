from psycopg import AsyncConnection
from datetime import datetime
from core.tables import Tables
from schemas.module_schemas import ModulesColumns
from schemas.organization_schemas import NewOrganization, CreateOrganization, OrganizationsColumns, UpdateOrganization, \
    DeleteOrganization, OrganizationStatus
from schemas.user_schemas import OrganizationUserColumns
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key


async def register_new_organization(
        connection: AsyncConnection,
        organization: NewOrganization,
        entity_id: str,
        creator: str,
        default: bool = False,
):
    with exception_response():
        __organization__ = CreateOrganization(
            id=get_unique_key(),
            name=organization.name,
            email=organization.email,
            type=organization.type,
            entity=entity_id,
            is_default=default,
            creator=creator,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ORGANIZATIONS.value)
            .values(__organization__)
            .check_exists({OrganizationsColumns.NAME.value: organization.name})
            .check_exists({OrganizationsColumns.EMAIL.value: organization.email})
            .returning(OrganizationsColumns.ID.value)
            .execute()
        )

        return builder



async def get_user_organizations(connection: AsyncConnection, user_id: str):
    with exception_response():

        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ORGANIZATIONS_USERS.value, alias="org_usr")
            .join(
                "LEFT",
                Tables.ORGANIZATIONS.value,
                "org.id = org_usr.organization_id",
                alias="org",
                use_prefix=False
            )
            .where("org_usr."+OrganizationUserColumns.USER_ID.value, user_id)
            .fetch_all()
        )
        return builder


async def get_entity_organizations(connection: AsyncConnection, entity_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ORGANIZATIONS.value, alias="org")
            .where("org."+OrganizationsColumns.ENTITY.value, entity_id)
            .fetch_all()
        )

        return builder


async def get_module_organization(connection: AsyncConnection, module_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES.value, alias="mod")
            .join(
                "LEFT",
                Tables.ORGANIZATIONS.value,
                "org.id = mod.organization",
                alias="org",
                use_prefix=False
            )
            .where("mod."+ModulesColumns.ID, module_id)
            .fetch_one()
        )

        return builder

async def get_organization_details(connection: AsyncConnection, organization_id: str):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ORGANIZATIONS.value, alias="org")
            .where("org."+OrganizationsColumns.ID.value, organization_id)
            .fetch_one()
        )

        return builder

async def edit_organization_details(connection: AsyncConnection, organization: UpdateOrganization, organization_id: str):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ORGANIZATIONS.value)
            .values(organization)
            .where({OrganizationsColumns.ID.value: organization_id})
            .check_exists({OrganizationsColumns.EMAIL.value: organization.email})
            .returning(OrganizationsColumns.ID.value)
            .execute()
        )

        return builder

async def delete_organization(connection: AsyncConnection, organization_id: str):
    with exception_response():
        __status__ = DeleteOrganization(
            status=OrganizationStatus.DELETED
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.ORGANIZATIONS.value)
            .values(__status__)
            .where({OrganizationsColumns.ID.value: organization_id})
            .check_exists({OrganizationsColumns.ID.value: organization_id})
            .returning(OrganizationsColumns.ID.value)
            .execute()
        )

        return builder
