import {
  ApiError,
  canTransition,
  parseStatus,
  requireEditor,
} from "../../../../src/domain.ts";

/** Example adapter around Fieldnotes' existing domain functions, not an HTTP API. */
export function transitionIssue(
  role: string,
  sessionWorkspace: string,
  issueWorkspace: string,
  currentStatus: string,
  requestedStatus: string,
): string {
  if (role === "anonymous" || sessionWorkspace === "") return "unauthenticated";
  if (role !== "editor" && role !== "viewer") return "forbidden";
  try {
    requireEditor(role);
  } catch (error) {
    if (error instanceof ApiError && error.status === 403) return "forbidden";
    throw error;
  }
  if (sessionWorkspace !== issueWorkspace) return "not_found";
  try {
    const current = parseStatus({ status: currentStatus });
    const requested = parseStatus({ status: requestedStatus });
    return canTransition(current, requested) ? requested : "invalid_transition";
  } catch (error) {
    if (error instanceof ApiError && error.status === 400)
      return "invalid_status";
    throw error;
  }
}
