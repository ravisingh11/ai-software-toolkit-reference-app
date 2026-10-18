package fieldnotes.domain

/** Pure authorization and transition decision; no transport or storage dependencies. */
object Transition {
  private val statuses: Set[String] = Set("triage", "in_progress", "done")

  def decide(
      role: String,
      sessionWorkspace: String,
      issueWorkspace: String,
      current: String,
      requested: String
  ): String = {
    if (role == "anonymous" || sessionWorkspace.isEmpty) "unauthenticated"
    else if (role != "editor") "forbidden"
    else if (sessionWorkspace != issueWorkspace) "not_found"
    else if (!statuses.contains(current) || !statuses.contains(requested)) "invalid_status"
    else if (current == requested || current == "in_progress" || requested == "in_progress") requested
    else "invalid_transition"
  }
}
