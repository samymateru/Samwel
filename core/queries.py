from psycopg import sql

querying_main_program_data = sql.SQL(
    """
        SELECT 
        mp.name AS program_name,
        mp.description as program_description,
        COALESCE(
          JSON_AGG(
            JSON_BUILD_OBJECT(
              'title', sp.title,
              'brief_description', sp.brief_description,
              'audit_objective', sp.audit_objective,
              'test_description', sp.test_description,
              'test_type', sp.test_type,
              'sampling_approach', sp.sampling_approach,
              'results_of_test', sp.results_of_test,
              'observation', sp.observation,
              'risk_control', COALESCE(
                  (
                    SELECT JSON_AGG(
                        JSON_BUILD_OBJECT(
                            'risk', pr.risk,
                            'risk_rating', pr.risk_rating,
                            'control', pr.control,
                            'control_type', pr.control_type,
                            'control_objective', pr.control_objective
                        )
                    )
                    FROM "PRCM" pr
                    WHERE pr.summary_audit_program = sp.id
                  ),
                  '[]'
              )
            )
          ) FILTER (WHERE sp.id IS NOT NULL),
          '[]'
        ) AS subPrograms
        FROM main_program mp
        LEFT JOIN sub_program sp ON sp.program = mp.id
        WHERE mp.id = %s
        GROUP BY mp.id, mp.name;
    """)


sub_program_fetch = sql.SQL(
    """
        SELECT 
        sp.title,
        sp.brief_description,
        sp.audit_objective,
        sp.test_description,
        sp.test_type,
        sp.sampling_approach,
        sp.results_of_test,
        sp.observation,
        COALESCE(
        JSON_AGG(
            JSON_BUILD_OBJECT(
			  	'risk', pr.risk,
				'risk_rating', pr.risk_rating,
				'control', pr.control,
				'control_type', pr.control_type,
				'control_objective', pr.control_objective
            )
        ) FILTER (WHERE pr.id IS NOT NULL),
        '[]'
        ) AS prcm
        FROM sub_program sp
        LEFT JOIN "PRCM" pr ON pr.summary_audit_program = sp.id
        WHERE sp.id = %s
        GROUP BY sp.id, sp.title, sp.brief_description, sp.audit_objective, 
         sp.test_description, sp.test_type, sp.sampling_approach, 
         sp.results_of_test, sp.observation;
    """)


risk_control_fetch = sql.SQL(
    """
    SELECT 
        pr.risk,
        pr.risk_rating,
        pr.control,
        pr.type,
        pr.control_objective
    FROM "PRCM" pr
    WHERE pr.id = %s;
    """)