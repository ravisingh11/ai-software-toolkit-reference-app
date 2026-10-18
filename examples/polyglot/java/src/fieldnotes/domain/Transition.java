package fieldnotes.domain;

import java.util.Set;

/** Pure authorization and status-transition rules; no persistence or I/O. */
public final class Transition {
    private static final Set<String> STATUSES = Set.of("triage", "in_progress", "done");

    private Transition() {
    }

    public static String apply(String role, String sessionWorkspace, String issueWorkspace,
            String current, String requested) {
        if ("anonymous".equals(role) || sessionWorkspace.isEmpty()) {
            return "unauthenticated";
        }
        if (!"editor".equals(role)) {
            return "forbidden";
        }
        if (!sessionWorkspace.equals(issueWorkspace)) {
            return "not_found";
        }
        if (!STATUSES.contains(current) || !STATUSES.contains(requested)) {
            return "invalid_status";
        }
        if (current.equals(requested) || "in_progress".equals(current)
                || "in_progress".equals(requested)) {
            return requested;
        }
        return "invalid_transition";
    }
}
