"""Pure Fieldnotes transition example, with no storage or authentication provider."""


def transition_issue(role: str, session_workspace: str, issue_workspace: str,
                     current_status: str, requested_status: str) -> str:
    if role == "anonymous" or not session_workspace:
        return "unauthenticated"
    if role != "editor":
        return "forbidden"
    if session_workspace != issue_workspace:
        return "not_found"
    statuses = {"triage", "in_progress", "done"}
    if current_status not in statuses or requested_status not in statuses:
        return "invalid_status"
    if current_status == requested_status or "in_progress" in (current_status, requested_status):
        return requested_status
    return "invalid_transition"
