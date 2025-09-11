from Management.subscriptions.schemas import EAuditLicence


plans = {
    "cb67a203f8da": EAuditLicence(
        licence_id="cb67a203f8da",
        name="Free Plan",
        audit_staff=2,
        business_staff=4,
        engagements_count=5,
        issues_count=20,
        email_count=20,
        follow_up=False,
        price = 10000
    ),

    "96ec62e67648": EAuditLicence(
        licence_id="96ec62e67648",
        name="Basic Plan",
        audit_staff=4,
        business_staff=10,
        engagements_count=20,
        issues_count=300,
        email_count=100,
        follow_up=False,
        price=250
    ),
    "60c50a6b7ccd": EAuditLicence(
        licence_id="60c50a6b7ccd",
        name="Professional Plan",
        audit_staff=8,
        business_staff=20,
        engagements_count=40,
        issues_count=1000,
        email_count=2000,
        follow_up=False,
        price=430
    ),
    "fd282e789a09": EAuditLicence(
        licence_id="fd282e789a09",
        name="Enterprise Plan",
        audit_staff=10000,
        business_staff=10000,
        engagements_count=10000,
        issues_count=10000,
        email_count=10000,
        follow_up=False,
        price=10000
    )
}


licences = [
    EAuditLicence(
        licence_id="cb67a203f8da",
        name="Free Plan",
        audit_staff=2,
        business_staff=4,
        engagements_count=5,
        issues_count=20,
        email_count=20,
        follow_up=False,
        price=0
    ),
    EAuditLicence(
        licence_id="96ec62e67648",
        name="Basic Plan",
        audit_staff=4,
        business_staff=10,
        engagements_count=20,
        issues_count=300,
        email_count=100,
        follow_up=False,
        price=250
    ),
    EAuditLicence(
        licence_id="60c50a6b7ccd",
        name="Professional Plan",
        audit_staff=8,
        business_staff=20,
        engagements_count=40,
        issues_count=1000,
        email_count=2000,
        follow_up=False,
        price=430
    ),
    EAuditLicence(
        licence_id="fd282e789a09",
        name="Enterprise Plan",
        audit_staff=100000,
        business_staff=10000,
        engagements_count=10000,
        issues_count=100000,
        email_count=10000,
        follow_up=False,
        price=10000
    )
]