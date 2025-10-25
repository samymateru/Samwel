"""
CREATE OR REPLACE FUNCTION update_plan_metrics()
RETURNS TRIGGER AS $$
DECLARE
    metrics_json JSONB;
    _module_id VARCHAR; -- adjust type if INT
    ref_plan_id VARCHAR;
BEGIN
    -- Determine the module_id depending on trigger table
    IF TG_TABLE_NAME = 'annual_plans' THEN
        _module_id := COALESCE(NEW.module, OLD.module);  -- annual_plans.module holds module_id

    ELSIF TG_TABLE_NAME = 'engagements' THEN
        ref_plan_id := COALESCE(NEW.plan_id, OLD.plan_id);
        SELECT p.module INTO _module_id FROM annual_plans p WHERE p.id = ref_plan_id;

    ELSE -- triggered from issue table
        SELECT p.module INTO _module_id
        FROM annual_plans p
        JOIN engagements e ON e.plan_id = p.id
        WHERE e.id = COALESCE(NEW.engagement, OLD.engagement);
    END IF;

    -- Skip if module_id not found
    IF _module_id IS NULL THEN
        RETURN NEW;
    END IF;

    -- Build JSON metrics filtered by module_id (through p.module)
    SELECT JSON_BUILD_OBJECT(
        'engagements_metrics', (
            SELECT JSON_BUILD_OBJECT(
                'total', COUNT(*),
                'pending', COUNT(*) FILTER (WHERE e.status = 'Pending'),
                'ongoing', COUNT(*) FILTER (WHERE e.status = 'Ongoing'),
                'completed', COUNT(*) FILTER (WHERE e.status = 'Completed'),
                'archived', COUNT(*) FILTER (WHERE e.status = 'Archived')
            )
            FROM engagements e
            JOIN annual_plans p ON p.id = e.plan_id
            WHERE p.module = _module_id
              AND p.year::int = (
                  SELECT MAX(year::int)
                  FROM annual_plans
                  WHERE module = _module_id
              )
              AND e.status NOT IN ('Deleted')
        ),
        'issues_metrics', (
            SELECT JSON_BUILD_OBJECT(
                'total', COUNT(*),
                'not_started', COUNT(*) FILTER (WHERE i.status = 'Not started'),
                'open', COUNT(*) FILTER (WHERE i.status IN ('Open', 'Active')),
                'in_progress', COUNT(*) FILTER (WHERE i.status = 'In progress'),
                'closed', COUNT(*) FILTER (WHERE i.status = 'Closed')
            )
            FROM issue i
            JOIN engagements e ON e.id = i.engagement
            JOIN annual_plans p ON p.id = e.plan_id
            WHERE p.module = _module_id
              AND p.year::int = (
                  SELECT MAX(year::int)
                  FROM annual_plans
                  WHERE module = _module_id
              )
              AND e.status NOT IN ('Deleted')
        )
    ) INTO metrics_json;

    -- Upsert result into plan_metrics
    INSERT INTO dashboards (id, metrics, updated_at)
    VALUES (_module_id, metrics_json, NOW())
    ON CONFLICT (id)
    DO UPDATE SET metrics = EXCLUDED.metrics, updated_at = NOW();

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

"""