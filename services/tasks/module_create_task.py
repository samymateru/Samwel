from constants import head_of_audit, administrator, member, business_manager, risk_manager, compliance_manager, \
    audit_reviewer, audit_lead, audit_member
from models.module_models import add_licence_to_module, generate_module_activation_data
from models.role_models import create_role_model
from schemas.module_schemas import NewModule, EAuditLicence
from services.connections.postgres.connections import AsyncDBPoolSingleton
from services.logging.logger import global_logger
from utils import exception_response


eaudit_roles = [
    head_of_audit,
    administrator,
    member,
    business_manager,
    risk_manager,
    compliance_manager,
    audit_reviewer,
    audit_lead,
    audit_member
]


async def module_create_task(
    module: NewModule,
    module_id: str,
    licence: EAuditLicence
):
    with exception_response():
        pool = await AsyncDBPoolSingleton.get_instance().get_pool()

        async with pool.connection() as connection:
            licence_data = await add_licence_to_module(
                connection=connection,
                module_id=module_id,
                plan_id=module.licence_id,
                licence=licence
            )


            if licence_data is None:
                global_logger.exception("Failed To Attach Licence To Module")


            activation_data = await generate_module_activation_data(
                connection=connection,
                module_id=module_id
            )


            if activation_data is None:
                global_logger.exception("Failed To Generate Activation Code")


            roles = [role.model_copy(update={"module": module_id}) for role in eaudit_roles]


            roles_data = await create_role_model(
                connection=connection,
                role=roles
            )

            if roles_data is None:
                global_logger.exception("Failed To Create Roles")



