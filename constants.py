from Management.roles.schemas import Section, Permissions, Archive, Type, Default
from datetime import datetime, timedelta
from schemas.role_schemas import CreateRole
from utils import get_unique_key


head_of_audit = CreateRole(
    id=get_unique_key(),
    reference="ROLE-001",
    default=Default.YES,
    name="Head of Audit",
    section=Section.E_AUDIT,
    type=Type.AUDIT,
    settings=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE,
    ],
    audit_plans=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    engagements=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    finalization=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    others=[Permissions.VIEW],
    archive_audit=Archive.YES,
    un_archive_audit=Archive.YES,
    created_at=datetime.now()
)


administrator = CreateRole(
    id=get_unique_key(),
    reference="ROLE-002",
    default=Default.YES,
    name="Administrator",
    section=Section.E_AUDIT,
    type=Type.AUDIT,
    settings=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE,
        Permissions.DELETE
    ],
    audit_plans=[Permissions.VIEW],
    engagements=[Permissions.VIEW],
    administration=[Permissions.VIEW],
    planning=[Permissions.VIEW],
    fieldwork=[Permissions.VIEW],
    reporting=[Permissions.VIEW],
    finalization=[Permissions.VIEW],
    audit_program=[Permissions.VIEW],
    follow_up=[Permissions.VIEW],
    issue_management=[Permissions.VIEW],
    others=[Permissions.VIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now()
)



member = CreateRole(
    id=get_unique_key(),
    reference="ROLE-003",
    default=Default.YES,
    name="Member",
    section=Section.E_AUDIT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    engagements=[Permissions.VIEW],
    administration=[Permissions.VIEW],
    planning=[Permissions.VIEW],
    fieldwork=[Permissions.VIEW],
    reporting=[Permissions.VIEW],
    finalization=[Permissions.VIEW],
    audit_program=[Permissions.VIEW],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    issue_management=[Permissions.VIEW],
    others=[Permissions.VIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.YES,
    created_at=datetime.now()
)


audit_lead = CreateRole(
    id=get_unique_key(),
    reference="ROLE-004",
    default=Default.YES,
    name="Audit Lead",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    engagements=[Permissions.VIEW],
    finalization=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    audit_program=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    follow_up=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    issue_management=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    others=[Permissions.VIEW, Permissions.REVIEW],
    archive_audit=Archive.NO,
    un_archive_audit=Archive.NO,
    created_at=datetime.now() + timedelta(seconds=1)
)


audit_reviewer = CreateRole(
    id=get_unique_key(),
    reference="ROLE-005",
    default=Default.YES,
    name="Audit Reviewer",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    engagements=[Permissions.VIEW],
    administration=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    planning=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    fieldwork=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
    ],
    reporting=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE
    ],
    finalization=[
        Permissions.VIEW,
        Permissions.CREATE,
        Permissions.EDIT,
        Permissions.DELETE,
        Permissions.APPROVE,
        Permissions.REVIEW
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


audit_member = CreateRole(
    id=get_unique_key(),
    reference="ROLE-006",
    default=Default.YES,
    name="Audit Member",
    section=Section.ENGAGEMENT,
    type=Type.AUDIT,
    settings=[Permissions.VIEW],
    audit_plans=[Permissions.VIEW],
    engagements=[Permissions.VIEW],
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
    finalization=[Permissions.VIEW],
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

business_manager = CreateRole(
    id=get_unique_key(),
    reference="ROLE-007",
    default=Default.YES,
    name="Business Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    engagements=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    finalization=[Permissions.VIEW],
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

risk_manager = CreateRole(
    id=get_unique_key(),
    reference="ROLE-008",
    default=Default.YES,
    name="Risk Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    engagements=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    finalization=[Permissions.VIEW],
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


compliance_manager = CreateRole(
    id=get_unique_key(),
    reference="ROLE-009",
    default=Default.YES,
    name="Compliance Manager",
    section=Section.E_AUDIT,
    type=Type.BUSINESS,
    settings=[],
    audit_plans=[],
    engagements=[],
    administration=[],
    planning=[],
    fieldwork=[],
    reporting=[],
    finalization=[Permissions.VIEW],
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



