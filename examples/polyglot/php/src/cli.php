<?php

declare(strict_types=1);

require_once __DIR__ . '/Domain/Transition.php';

use Fieldnotes\Domain\Transition;

while (($line = fgets(STDIN)) !== false) {
    $fields = explode("\t", rtrim($line, "\r\n"));
    if (count($fields) !== 6) {
        fwrite(STDERR, "Expected six TSV fields\n");
        exit(2);
    }
    [$id, $role, $session, $workspace, $current, $requested] = $fields;
    echo $id . "\t" . Transition::apply($role, $session, $workspace, $current, $requested) . "\n";
}
