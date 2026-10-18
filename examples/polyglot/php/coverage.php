<?php

declare(strict_types=1);

// Xdebug instruments executable lines, including unexecuted and dead code.
xdebug_set_filter(XDEBUG_FILTER_CODE_COVERAGE, XDEBUG_PATH_INCLUDE, [__DIR__ . '/src/']);
xdebug_start_code_coverage(XDEBUG_CC_UNUSED | XDEBUG_CC_DEAD_CODE);
require __DIR__ . '/src/cli.php';
$data = xdebug_get_code_coverage();
xdebug_stop_code_coverage();
$xml = new SimpleXMLElement('<coverage/>');
$xml->addAttribute('version', 'xdebug-' . phpversion('xdebug'));
$xml->addAttribute('timestamp', (string) time());
$xml->addAttribute('branch-rate', '0');
$xml->addChild('sources')->addChild('source', '.');
$package = $xml->addChild('packages')->addChild('package');
$package->addAttribute('name', 'php');
$classes = $package->addChild('classes');
$covered = 0;
$total = 0;
foreach ($data as $file => $lines) {
    if (!str_starts_with($file, __DIR__ . '/src/')) {
        continue;
    }
    $class = $classes->addChild('class');
    $class->addAttribute('filename', substr($file, strlen(getcwd()) + 1));
    $class->addAttribute('name', basename($file));
    $class->addChild('methods');
    $nodes = $class->addChild('lines');
    $fileCovered = 0;
    $fileTotal = 0;
    $sourceLineCount = count(file($file));
    foreach ($lines as $number => $hit) {
        // PHP 8.4/Xdebug emits a covered implicit file return at EOF + 1.
        // It has no physical source line. Never discard an unexecuted line.
        if ($number === $sourceLineCount + 1 && $hit > 0) {
            continue;
        }
        if ($number < 1 || $number > $sourceLineCount) {
            throw new RuntimeException('Unexpected coverage line outside source: ' . $file);
        }
        if ($hit === -2) {
            continue; // Xdebug identifies this as non-executable dead code.
        }
        $node = $nodes->addChild('line');
        $node->addAttribute('number', (string) $number);
        $node->addAttribute('hits', $hit > 0 ? '1' : '0');
        $fileCovered += $hit > 0 ? 1 : 0;
        $fileTotal++;
    }
    $class->addAttribute('line-rate', (string) ($fileTotal > 0 ? $fileCovered / $fileTotal : 0));
    $class->addAttribute('branch-rate', '0');
    $covered += $fileCovered;
    $total += $fileTotal;
}
if ($total === 0) {
    throw new RuntimeException('No executable PHP lines collected');
}
$xml->addAttribute('lines-covered', (string) $covered);
$xml->addAttribute('lines-valid', (string) $total);
$xml->addAttribute('line-rate', (string) ($covered / $total));
$package->addAttribute('line-rate', (string) ($covered / $total));
$package->addAttribute('branch-rate', '0');
$report = getenv('POLYGLOT_COVERAGE_REPORT');
if ($report === false || $report === '' || !$xml->asXML($report)) {
    throw new RuntimeException('Unable to write coverage report');
}
