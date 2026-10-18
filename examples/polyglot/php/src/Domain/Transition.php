<?php

declare(strict_types=1);

namespace Fieldnotes\Domain;

final class Transition
{
    public static function apply(
        string $role,
        string $sessionWorkspace,
        string $issueWorkspace,
        string $current,
        string $requested,
    ): string {
        if ($role === 'anonymous' || $sessionWorkspace === '') {
            return 'unauthenticated';
        }
        if ($role !== 'editor') {
            return 'forbidden';
        }
        if ($sessionWorkspace !== $issueWorkspace) {
            return 'not_found';
        }
        $statuses = ['triage', 'in_progress', 'done'];
        if (!in_array($current, $statuses, true) || !in_array($requested, $statuses, true)) {
            return 'invalid_status';
        }
        if ($current === $requested || $current === 'in_progress' || $requested === 'in_progress') {
            return $requested;
        }
        return 'invalid_transition';
    }
}
