from psycopg import AsyncConnection
from Management.subscriptions.schemas import EAuditLicence, CreateLicence
from services.connections.insert_builder import InsertQueryBuilder
from utils import exception_response, get_unique_key


async def attach_licence_to_module(connection: AsyncConnection, licence: EAuditLicence, module_id: str):
    with exception_response():
        __licence_data__ = CreateLicence(
            licence_id=get_unique_key(),
            module_id=module_id,
            name=licence.name,
            audit_staff=licence.audit_staff,
            business_staff=licence.business_staff,
            engagements_count=licence.engagements_count,
            issues_count=licence.issues_count,
            emails_count=licence.emails_count,
            follow_up=licence.follow_up,
            price=licence.price
        )

        builder = (
            InsertQueryBuilder(connection=connection)
            .into_table("audit_licences")
            .values(__licence_data__)
            .returning("licence_id")
        )

        return await builder.execute()

