from collections import Counter
from dataclasses import dataclass
from typing import List

from AuditNew.Internal.dashboards.schemas import _Issue_, IssueStatusSummary


def count_issue_statuses(rows: List[_Issue_]):
    status_counter = Counter()

    for row in rows:

        # Normalize status into broader categories
        if row.status == "Not started":
            status_counter["Not started"] += 1
        elif row.status == "Open":
            status_counter["Open"] += 1
        elif row.status.startswith("In progress"):
            status_counter["In Progress"] += 1
        elif row.status.startswith("Closed"):
            status_counter["Closed"] += 1

    return IssueStatusSummary(
        total=sum(status_counter.values()),
        not_started=status_counter.get("Not started", 0),
        open=status_counter.get("Open", 0),
        in_progress=status_counter.get("In Progress", 0),
        closed=status_counter.get("Closed", 0),
    )

