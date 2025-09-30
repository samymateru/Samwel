from psycopg import AsyncConnection
from schemas.standard_template_schemas import NewStandardTemplate, TemplateType, ProcedureTypes, CreateStandardTemplate, \
    Section, TemplateStatus, StandardTemplateColumns, UpdateStandardProcedure
from services.connections.postgres.delete import DeleteQueryBuilder
from services.connections.postgres.insert import InsertQueryBuilder
from services.connections.postgres.read import ReadBuilder
from services.connections.postgres.update import UpdateQueryBuilder
from utils import exception_response, get_unique_key

procedure_category = {
    "Planning": "std_template",
    "Reporting": "reporting_procedure",
    "Finalization": "finalization_procedure"
}



async def create_new_standard_template_model(
        connection: AsyncConnection,
        template: NewStandardTemplate,
        type_: ProcedureTypes,
        engagement_id: str
):
    with exception_response():
        __standard_template__ = CreateStandardTemplate(
            id=get_unique_key(),
            engagement=engagement_id,
            title=template.title,
            reference="",
            tests=Section(value=""),
            objectives = Section(value=""),
            observation = Section(value=""),
            results=Section(value=""),
            conclusion=Section(value=""),
            type=TemplateType.STANDARD,
            status=TemplateStatus.PENDING,
            prepared_by=None,
            reviewed_by=None
        )

        builder = await (
            InsertQueryBuilder(connection=connection)
            .into_table(procedure_category.get(type_.value))
            .check_exists({StandardTemplateColumns.ENGAGEMENT.value: engagement_id})
            .check_exists({StandardTemplateColumns.TITLE.value: template.title})
            .returning(StandardTemplateColumns.ID.value)
            .values(__standard_template__)
            .execute()
        )

        return builder



async def delete_standard_template_model(
        connection: AsyncConnection,
        type_: ProcedureTypes,
        procedure_id: str,
):
    with exception_response():
        builder = await (
            DeleteQueryBuilder(connection=connection)
            .from_table(procedure_category.get(type_.value))
            .check_exists({StandardTemplateColumns.ID.value: procedure_id})
            .where({StandardTemplateColumns.ID.value: procedure_id})
            .returning(StandardTemplateColumns.ID.value)
            .execute()
        )

        return builder



async def update_standard_template_model(
        connection: AsyncConnection,
        type_: ProcedureTypes,
        procedure: UpdateStandardProcedure,
        procedure_id: str,
):
    with exception_response():
        builder = await (
            UpdateQueryBuilder(connection=connection)
            .into_table(procedure_category.get(type_.value))
            .values(procedure)
            .check_exists({StandardTemplateColumns.ID.value: procedure_id})
            .where({StandardTemplateColumns.ID.value: procedure_id})
            .returning(StandardTemplateColumns.ID.value)
            .execute()
        )

        return builder



async def read_standard_template_model(
        connection: AsyncConnection,
        type_: ProcedureTypes,
        engagement_id: str,
):
    with exception_response():
        builder = await (
            ReadBuilder(connection=connection)
            .from_table(procedure_category.get(type_.value))
            .where(StandardTemplateColumns.ENGAGEMENT.value, engagement_id)
            .fetch_all()
        )

        return builder
