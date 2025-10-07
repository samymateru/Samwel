from typing import Any

from psycopg import AsyncConnection
from core.tables import Tables
from schemas.module_schemas import NewModule, CreateModule, ModuleStatus, ModulesColumns, CreateModuleActivation, \
    ActivationColumns, ActivateModule, CreateAuditLicence, AuditLicenceColumns, EAuditLicence, DeleteModuleTemporarily, \
    ModuleDataReference, ReadLicence, BaseModule
from schemas.user_schemas import ModuleUserColumns
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key
from datetime import datetime


async def register_new_module(
        connection: AsyncConnection,
        module: NewModule,
        organization_id: str,
        status: ModuleStatus
):
    with exception_response():
        __module__ = CreateModule(
            id=get_unique_key(),
            organization=organization_id,
            name=module.name,
            status=status.value,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.MODULES)
            .values(__module__)
            .check_exists({ModulesColumns.NAME.value: module.name})
            .check_exists({ModulesColumns.ORGANIZATION.value: organization_id})
            .returning(ModulesColumns.ID.value)
            .execute()
        )

        return builder


async def get_user_modules(
        connection: AsyncConnection,
        user_id: str,
        organization_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES_USERS.value, alias="mod_usr")
            .join(
                "LEFT",
                Tables.MODULES.value,
                "mod.id = mod_usr.module_id",
                alias="mod",
                use_prefix=False
            )
            .where("mod_usr."+ModuleUserColumns.USER_ID.value, user_id)
            .where("mod_usr." + ModuleUserColumns.ORGANIZATION_ID.value, organization_id)

            .fetch_all()
        )
        return builder


async def get_organization_modules(
        connection: AsyncConnection,
        organization_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES.value, alias="mod")
            .select(BaseModule)
            .join(
                "LEFT",
                "audit_licences",
                "licence.module_id = mod.id",
                "licence",
                use_prefix=True,
                model=ReadLicence
            )
            .select_joins()
            .where("mod."+ModulesColumns.ORGANIZATION.value, organization_id)
            .fetch_all()
        )
        return builder



async def get_module_details(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES.value, alias="mod")
            .where("mod."+ModulesColumns.ID.value, module_id)
            .fetch_one()
        )
        return builder



async def generate_module_activation_data(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        __activation_module__ = CreateModuleActivation(
            activation_token=get_unique_key().upper(),
            module_id=module_id,
            created_at=datetime.now()
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.ACTIVATIONS.value)
            .values(__activation_module__)
            .check_exists({ActivationColumns.MODULE_ID.value: module_id})
            .returning(ActivationColumns.MODULE_ID.value)
            .execute()
        )

        return builder




async def activate_module(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        __activate_module__ = ActivateModule(
            status=ModuleStatus.ACTIVE,
            purchase_date=datetime.now()
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MODULES.value)
            .values(__activate_module__)
            .where({ModulesColumns.ID.value: module_id})
            .check_exists({ModulesColumns.ID.value: module_id})
            .returning(ModulesColumns.ID.value)
            .execute()
        )

        return builder


async def get_activation_data(
        connection: AsyncConnection,
        activation_token: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.ACTIVATIONS.value)
            .where(ActivationColumns.ACTIVATION_TOKEN.value, activation_token)
            .fetch_one()
        )

        return builder


async def add_licence_to_module(
        connection: AsyncConnection,
        module_id: str,
        licence: EAuditLicence,
        plan_id: str

):
    with exception_response():
        __module_licence__ = CreateAuditLicence(
            licence_id=get_unique_key(),
            module_id=module_id,
            plan_id=plan_id,
            name=licence.name,
            audit_staff=licence.audit_staff,
            business_staff=licence.business_staff,
            engagements_count=licence.engagements_count,
            emails_count=licence.emails_count,
            issues_count=licence.issues_count,
            price=licence.price,
            follow_up=licence.follow_up,
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(Tables.AUDIT_LICENCES.value)
            .values(__module_licence__)
            .check_exists({AuditLicenceColumns.MODULE_ID.value: module_id})
            .returning(AuditLicenceColumns.LICENCE_ID.value)
            .execute()
        )

        return builder



async def get_module_licence_data(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.AUDIT_LICENCES.value)
            .where(AuditLicenceColumns.MODULE_ID.value, module_id)
            .fetch_one()
        )

        return builder


async def delete_module_temporarily_model(
        connection: AsyncConnection,
        module_id: str
):
    with exception_response():
        __module__ = DeleteModuleTemporarily(
            status=ModuleStatus.CLOSED
        )

        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MODULES.value)
            .values(__module__)
            .check_exists({ModulesColumns.ID.value: module_id})
            .where({ModulesColumns.ID.value: module_id})
            .returning(ModulesColumns.ID.value)
            .execute()
        )

        return builder


async def increment_module_reference(
        connection: AsyncConnection,
        module_id: str,
        value: Any
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(Tables.MODULES.value)
            .values(value)
            .check_exists({ModulesColumns.ID.value: module_id})
            .where({ModulesColumns.ID.value: module_id})
            .returning(ModulesColumns.ID.value)
            .execute()
        )
        return builder


async def get_data_reference_in_module(
        connection: AsyncConnection,
        module_id: str,
        sections: ModuleDataReference
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(Tables.MODULES.value)
            .select_fields(sections.value)
            .where(ModulesColumns.ID.value, module_id)
            .fetch_one()
        )

        return int(builder.get(sections))