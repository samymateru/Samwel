from Management.roles.schemas import Roles, Section, Permissions, Archive, Type, Default
from datetime import datetime, timedelta

head_of_audit = Roles(
    id="ROLE-001",
    reference="ROLE-001",
    default=Default.YES,
    name="Head of Audit",
    section=Section.E_AUDIT,
    type=Type.AUDIT,
    settings=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    audit_plans=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    others=[Permissions.VIEW],
    archive_audit=Archive.YES,
    un_archive_audit=Archive.YES,
    created_at=datetime.now()
)

audit_lead = Roles(
    id="ROLE-002",
    reference="ROLE-002",
    default=Default.YES,
    name="Audit Lead",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    others=[Permissions.VIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=1)
)


audit_reviewer = Roles(
    id="ROLE-003",
    reference="ROLE-003",
    default=Default.YES,
    name="Audit Reviewer",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    others=[Permissions.VIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=2)
)

audit_member = Roles(
    id="ROLE-004",
    reference="ROLE-004",
    default=Default.YES,
    name="Audit Member",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    administration=[Permissions.VIEW],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    others=[Permissions.VIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=3)
)

business_manager = Roles(
    id="ROLE-005",
    reference="ROLE-005",
    default=Default.YES,
    name="Business Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    audit_program=[],
    follow_up=[],
    issue_management=[
        Permissions.VIEW,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    others=[],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=6)
)

risk_manager = Roles(
    id="ROLE-006",
    reference="ROLE-006",
    default=Default.YES,
    name="Risk Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    audit_program=[],
    follow_up=[],
    issue_management=[
        Permissions.VIEW,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    others=[],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=6)
)

compliance_manager = Roles(
    id="ROLE-007",
    reference="ROLE-007",
    default=Default.YES,
    name="Compliance Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    audit_program=[],
    follow_up=[],
    issue_management=[
        Permissions.VIEW,
        Permissions.EDIT,
        Permissions.APPROVE
    ],
    others=[],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=6)
)

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


data_roles = {
    "name": "name",
    "permission": [
        {"name": [""]}
    ]
}


roles_ = {
    "name": "Owner",
    "permission": [
        {"user-roles": ["create", "view", "delete", "update", "assign", "approve"]},
        {"account-profile": ["create", "view", "delete", "update", "assign", "approve"]},
        {"subscription": ["create", "view", "delete", "update", "assign", "approve"]}
    ]
}



value = [
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
        {
            "name": "Admin",
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
        {
            "name": "Chief Executive Officer",
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
        {
            "name": "Chief Financial Officer",
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
        {
            "name": "Chief Information Officer",
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
        {
            "name": "Chief Operation Officer",
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
        {
            "name":"Chief Information Security Officer",
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
        {
            "name": "Head of Audit",
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
        {
            "name": "Senior Audit Manager",
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
        {
            "name": "Risk Manager",
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
        }
   ]
