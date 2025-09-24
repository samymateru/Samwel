from datetime import datetime
from psycopg import AsyncConnection, sql
from core.tables import Tables
from schemas.user_schemas import NewUser, CreateUser, UserStatus, UserColumns, CreateOrganizationUser, \
    OrganizationUserColumns, CreateModuleUser, ModuleUserColumns, UpdateModuleUser, UpdateEntityUser
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from services.security.security import hash_password
from utils import exception_response, get_unique_key


async def register_new_user(
        connection: AsyncConnection,
        user: NewUser,
        entity_id: str,
        check_if_exist: bool = True,
        password: str = "123456",
        administrator = False,
        owner = False
):
    with exception_response():
        __user__ = CreateUser(
            id=get_unique_key(),
            entity=entity_id,
            name=user.name,
            email=user.email,
            telephone=user.telephone,
            status=UserStatus.NEW,
            administrator=administrator,
            owner=owner,
            image="",
            password_hash=hash_password(password),
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.USERS)
            .values(__user__)
            .check_exists({UserColumns.EMAIL.value: user.email})
            .throw_error_on_exists(check_if_exist)
            .returning(UserColumns.ID.value)
            .execute()
        )

        return builder


async def create_new_organization_user(
        connection: AsyncConnection,
        organization_id: str,
        user_id: str,
        administrator: bool = False,
        owner: bool = False,
        check_exists: bool = False
):
    with exception_response():
        __organization_user__ = CreateOrganizationUser(
            organization_user_id=get_unique_key(),
            organization_id=organization_id,
            user_id=user_id,
            administrator=administrator,
            owner=owner,
            created_at=datetime.now()
        )

        builder =  await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ORGANIZATIONS_USERS.value)
            .values(__organization_user__)
            .check_exists({OrganizationUserColumns.USER_ID.value: user_id})
            .check_exists({OrganizationUserColumns.ORGANIZATION_ID.value: organization_id})
            .throw_error_on_exists(check_exists)
            .returning(OrganizationUserColumns.ORGANIZATION_USER_ID.value)
            .execute()
        )

        return builder


async def create_new_module_user(
        connection: AsyncConnection,
        module_id: str,
        user_id: str,
        user: NewUser,
        check_exists: bool = True
):
    with exception_response():
        __module_user__ = CreateModuleUser(
            module_user_id=get_unique_key(),
            module_id=module_id,
            user_id=user_id,
            role=user.role,
            title=user.title,
            type=user.type,
            created_at=datetime.now()
        )

        builder =  await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.MODULES_USERS.value)
            .values(__module_user__)
            .check_exists({ModuleUserColumns.USER_ID.value: user_id})
            .check_exists({ModuleUserColumns.MODULE_ID.value: module_id})
            .throw_error_on_exists(check_exists)
            .returning(ModuleUserColumns.MODULE_USER_ID.value)
            .execute()
        )

        return builder


async def get_module_users(
        connection: AsyncConnection,
        module_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES_USERS.value, alias="mod_usr")
            .join(
                "LEFT",
                Tables.USERS,
                "usr.id = mod_usr.user_id",
                "usr",
                use_prefix=False
            )
            .where("mod_usr."+ModuleUserColumns.MODULE_ID, module_id)
            .fetch_all()
        )

        return builder


async def get_organization_users(
        connection: AsyncConnection,
        organization_id: str,
):
    query = sql.SQL("""
        SELECT 
          usr.id,
          usr.entity,
          org_usr.organization_id AS organization,
          usr.name,
          usr.status,
          usr.image,
          usr.email,
          usr.telephone,
          usr.created_at,
          org_usr.administrator,
          org_usr.owner,
          COALESCE(
            JSON_AGG(
              JSON_BUILD_OBJECT(
                'id',    mod.id,
                'title', mod_usr.title,
                'role',  mod_usr.role,
                'type',  mod_usr.type,
                'name',  mod.name
              )
            ) FILTER (WHERE mod_usr.module_id IS NOT NULL),
            '[]'::json
          ) AS modules
        FROM public.organizations_users org_usr
        JOIN public.users usr 
          ON usr.id = org_usr.user_id
        LEFT JOIN public.modules_users mod_usr 
          ON mod_usr.user_id = usr.id
        LEFT JOIN public.modules mod 
          ON mod.id = mod_usr.module_id
        WHERE org_usr.organization_id = %(org_id)s
        GROUP BY 
          usr.id,
          usr.entity,
          org_usr.organization_id,
          usr.name,
          usr.image,
          usr.status,
          usr.email,
          usr.telephone,
          usr.created_at,
          org_usr.administrator,
          org_usr.owner
    """)

    async with connection.cursor() as cursor:
        await cursor.execute(query, {"org_id": organization_id})
        rows = await cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]
        return result


async def get_entity_users(
        connection: AsyncConnection,
        entity_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.USERS.value)
            .where(UserColumns.ENTITY.value, entity_id)
            .fetch_all()
        )

        return builder


async def get_module_user_details(
        connection: AsyncConnection,
        module_id: str,
        user_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES_USERS.value, alias="mod_usr")
            .join(
                "LEFT",
                Tables.USERS,
                "usr.id = mod_usr.user_id",
                "usr",
                use_prefix=False
            )
            .where("mod_usr."+ModuleUserColumns.MODULE_ID.value, module_id)
            .where("usr."+UserColumns.ID.value, user_id)
            .fetch_one()
        )

        return builder


async def get_entity_user_details_by_mail(
        connection: AsyncConnection,
        email: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.USERS.value)
            .where(UserColumns.EMAIL.value, email)
            .fetch_one()
        )

        return builder


async def delete_user_in_module(
        connection: AsyncConnection,
        user_id: str,
        module_id: str,
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(Tables.MODULES_USERS.value)
            .check_exists({ModuleUserColumns.USER_ID.value: user_id})
            .where({
                ModuleUserColumns.USER_ID.value: user_id,
                ModuleUserColumns.MODULE_ID.value: module_id
            })
            .returning(ModuleUserColumns.USER_ID.value)
            .execute()
        )

        return  builder


async def edit_module_user(
        connection: AsyncConnection,
        user: UpdateModuleUser,
        user_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MODULES_USERS.value)
            .values(user)
            .check_exists({ModuleUserColumns.USER_ID.value: user_id})
            .where({ModuleUserColumns.USER_ID.value: user_id})
            .returning(ModuleUserColumns.USER_ID.value)
            .execute()
        )

        return builder


async def edit_entity_user(
        connection: AsyncConnection,
        user: UpdateEntityUser,
        user_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.USERS.value)
            .values(user)
            .check_exists({UserColumns.ID.value: user_id})
            .where({UserColumns.ID.value: user_id})
            .returning(UserColumns.ID.value)
            .execute()
        )

        return builder