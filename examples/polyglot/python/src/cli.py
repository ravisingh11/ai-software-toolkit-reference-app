"""TSV transport for the shared, externally asserted conformance cases."""
import sys

from .domain import transition_issue

for line in sys.stdin:
    fields = line.rstrip("\n").split("\t")
    if len(fields) != 6:
        raise ValueError("Expected six TSV fields")
    case_id, role, session, issue, current, requested = fields
    print(case_id + "\t" + transition_issue(role, session, issue, current, requested))
