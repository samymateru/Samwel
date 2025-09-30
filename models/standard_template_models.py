from psycopg import AsyncConnection
from schemas.standard_template_schemas import NewStandardTemplate, TemplateType, ProcedureTypes
from services.connections.postgres.insert import InsertQueryBuilder
from utils import exception_response

procedure_category = {
    "Planning": "std_template",
    "Reporting": "reporting_procedure",
    "Finalization": "finalization_procedure"
}

async def create_new_standard_template_model(
        connection: AsyncConnection,
        template: NewStandardTemplate,
        procedure: ProcedureTypes,
        engagement_id: str
):
    with exception_response():
        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(procedure_category.get(procedure.value))
            .execute()
        )

        return builder