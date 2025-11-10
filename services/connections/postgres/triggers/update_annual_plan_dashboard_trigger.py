from services.connections.postgres.connections import AsyncPGPoolSingleton
from utils import exception_response



async def update_annual_plan_dashboard_trigger():
    with exception_response():
        pool_singleton = await AsyncPGPoolSingleton.get_instance()
        async for connection in pool_singleton.get_db_connection():
            await connection.execute(
                """
                CREATE OR REPLACE FUNCTION annual_plan_metrics()
                RETURNS TRIGGER AS $$
                DECLARE
                    summary_json JSONB;
                    _plan_id VARCHAR;
                BEGIN
                    -- Determine the affected plan_id depending on operation type
                    IF (TG_OP = 'DELETE') THEN
                        _plan_id := OLD.plan_id;
                    ELSE
                        _plan_id := NEW.plan_id;
                    END IF;
                
                    -- Compute the summary
                    SELECT jsonb_build_object(
                        'total', COUNT(*),
                        'pending', COUNT(*) FILTER (WHERE e.status = 'Pending'),
                        'ongoing', COUNT(*) FILTER (WHERE e.status = 'Ongoing'),
                        'completed', COUNT(*) FILTER (WHERE e.status IN ('Completed', 'Archived'))
                    )
                    INTO summary_json
                    FROM engagements e
                    WHERE e.plan_id = _plan_id
                      AND e.status NOT IN ('Deleted');
                
                    -- Upsert the summary into plan_summaries
                    INSERT INTO annual_plan_dashboard (plan_id, metrics, updated_at)
                    VALUES (_plan_id, summary_json, NOW())
                    ON CONFLICT (plan_id)
                    DO UPDATE SET
                        metrics = EXCLUDED.metrics,
                        updated_at = NOW();
                
                    RETURN NULL;
                END;
                $$ LANGUAGE plpgsql;
                """)

            await connection.execute(
                """
                DROP TRIGGER IF EXISTS trg_update_plan_dashboard ON engagements;

                CREATE TRIGGER trg_update_plan_dashboard
                AFTER INSERT OR UPDATE OR DELETE ON engagements
                FOR EACH ROW
                EXECUTE FUNCTION annual_plan_metrics();
                """
            )

