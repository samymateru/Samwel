from fastapi import Depends
from services.connections.postgres.connections import get_asyncpg_db_connection, DBConnection
from utils import exception_response


async def manage_staff_limits(connection: DBConnection = Depends(get_asyncpg_db_connection)):
    with exception_response():
        """
        CREATE OR REPLACE FUNCTION public.manage_staff_limits()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
    target_column text;
    available_count int;
BEGIN
    -- Determine which column to update
    IF TG_OP = 'INSERT' THEN
        IF NEW.type = 'audit' THEN
            target_column := 'audit_staff';
        ELSIF NEW.type = 'business' THEN
            target_column := 'business_staff';
        ELSE
            RAISE EXCEPTION 'Unknown user type: %', NEW.type;
        END IF;

        -- Check availability and capture the count
        EXECUTE format('SELECT %I FROM audit_licences WHERE module_id = $1', target_column)
        INTO available_count
        USING NEW.module_id;

        IF available_count IS NULL OR available_count <= 0 THEN
            RAISE EXCEPTION 'User limit reached for module % and type %', NEW.module_id, NEW.type;
        END IF;

        -- Decrement the appropriate column
        EXECUTE format('UPDATE audit_licences SET %I = %I - 1 WHERE module_id = $1', target_column, target_column)
        USING NEW.module_id;

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        IF OLD.type = 'audit' THEN
            target_column := 'audit_staff';
        ELSIF OLD.type = 'business' THEN
            target_column := 'business_staff';
        ELSE
            RAISE EXCEPTION 'Unknown user type: %', OLD.type;
        END IF;

        -- Increment the appropriate column
        EXECUTE format('UPDATE audit_licences SET %I = %I + 1 WHERE module_id = $1', target_column, target_column)
        USING OLD.module_id;

        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$;

ALTER FUNCTION public.manage_staff_limits() OWNER TO postgres;



DROP TRIGGER IF EXISTS trg_manage_staff_limits ON modules_users;

CREATE TRIGGER trg_manage_staff_limits
AFTER INSERT OR DELETE
ON modules_users
FOR EACH ROW
EXECUTE FUNCTION public.manage_staff_limits();
        """