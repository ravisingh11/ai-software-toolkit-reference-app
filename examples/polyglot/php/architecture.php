<?php

declare(strict_types=1);

// Conservative syntax boundary: pure domain files cannot import dependencies,
// perform I/O, instantiate classes, or make dynamic calls. Not a whole-program graph.
$allowedNames = ['Fieldnotes\\Domain', 'in_array'];
$blockedTokens = [T_USE, T_REQUIRE, T_REQUIRE_ONCE, T_INCLUDE, T_INCLUDE_ONCE,
    T_NEW, T_EVAL, T_GLOBAL, T_ECHO, T_PRINT, T_EXIT, T_DOUBLE_COLON, T_OBJECT_OPERATOR,
    T_NULLSAFE_OBJECT_OPERATOR, T_VARIABLE];
$files = [];
$iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator(__DIR__ . '/src/Domain'));
foreach ($iterator as $entry) {
    if ($entry->isFile() && $entry->getExtension() === 'php') {
        $files[] = $entry->getPathname();
    }
}
if ($files === []) {
    throw new RuntimeException('No domain files discovered');
}
foreach ($files as $file) {
    $tokens = token_get_all(file_get_contents($file), TOKEN_PARSE);
    foreach ($tokens as $index => $token) {
        if ($token === '`') {
            throw new RuntimeException('Shell execution is forbidden in the domain');
        }
        if (!is_array($token)) {
            continue;
        }
        [$type, $text, $line] = $token;
        $next = $index + 1;
        while (isset($tokens[$next]) && is_array($tokens[$next]) && in_array($tokens[$next][0], [T_WHITESPACE, T_COMMENT, T_DOC_COMMENT], true)) {
            $next++;
        }
        $blocked = in_array($type, $blockedTokens, true);
        if ($type === T_VARIABLE) {
            $blocked = ($tokens[$next] ?? null) === '(';
        }
        if (in_array($type, [T_NAME_QUALIFIED, T_NAME_FULLY_QUALIFIED, T_NAME_RELATIVE], true)) {
            $blocked = !in_array($text, $allowedNames, true);
        }
        if ($type === T_STRING && ($tokens[$next] ?? null) === '(' && !in_array($text, ['apply', 'in_array'], true)) {
            $blocked = true;
        }
        if ($blocked) {
            fwrite(STDERR, "$file:$line: forbidden domain dependency or effect: $text\n");
            exit(1);
        }
    }
}
echo "PHP token architecture boundary passed\n";
