values = [
 {
            "name": "Owner",
            "creator": "Owner",
            "categories": [
                {
                    "name": "eAudit_Setting",
                    "permissions": {
                        "user_roles": ["view", "edit", "delete", "assign", "approve"],
                        "profile": ["view", "edit", "delete", "assign", "approve"],
                        "subscription": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "planning",
                    "permissions": {
                        "audit_plan": ["view", "edit", "delete", "assign", "approve"],
                        "audit_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "fieldwork",
                    "permissions": {
                        "fieldwork_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "reporting",
                    "permissions": {
                        "send_audit_findings": ["view", "edit", "delete", "assign", "approve"],
                        "reporting_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "finalization",
                    "permissions": {
                        "procedures": ["view", "edit", "delete", "assign", "approve"],
                        "archive_audit_files": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "audit_procedures",
                    "permissions": {
                        "manage_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                },
                {
                    "name": "follow_up",
                    "permissions": {
                        "reopen": ["view", "edit", "delete", "assign", "approve"],
                        "follow_up_procedures": ["view", "edit", "delete", "assign", "approve"],
                    }
                }
            ]
        },

]