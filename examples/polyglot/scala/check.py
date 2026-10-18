"""Pinned, offline-after-setup Scala example tooling."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
CACHE = ROOT / '.artifacts/polyglot/scala'
TOOLS = json.loads((LANE / 'toolchain.json').read_text())
JAVA_HOME = os.environ.get('JAVA_HOME', '/opt/homebrew/opt/openjdk@21')
JAVA = str(Path(JAVA_HOME) / 'bin/java') if Path(JAVA_HOME, 'bin/java').exists() else 'java'
JDEPS = str(Path(JAVA_HOME) / 'bin/jdeps') if Path(JAVA_HOME, 'bin/jdeps').exists() else 'jdeps'
CLASSES = CACHE / 'classes'
LIBRARY = CACHE / 'scala-library-2.13.16.jar'


def run(args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)


def tools_ready():
    for tool in TOOLS:
        path = CACHE / tool['file']
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != tool['sha256']:
            raise SystemExit('Missing or corrupt Scala tool; run check.sh setup: ' + tool['file'])


def compile_sources(lint=False):
    target = CACHE / ('lint-classes' if lint else 'classes')
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    args = [JAVA, '-cp', str(CACHE / '*'), 'scala.tools.nsc.Main', '-classpath', str(LIBRARY),
            '-deprecation', '-feature', '-unchecked', '-Werror', '-d', str(target)]
    if lint:
        args += ['-Xplugin:' + str(CACHE / 'wartremover_2.13.16-3.3.4.jar')]
        args += ['-P:wartremover:traverser:org.wartremover.warts.' + rule
                 for rule in ['Null', 'Var', 'Return', 'AsInstanceOf', 'IsInstanceOf', 'OptionPartial', 'TryPartial']]
    run(args + [str(p) for p in sorted((LANE / 'src').rglob('*.scala'))], stdout=sys.stderr)


def application(agent=None):
    args = [JAVA]
    if agent:
        args.append('-javaagent:' + str(CACHE / 'org.jacoco.agent-0.8.13-runtime.jar')
                    + '=destfile=' + str(agent) + ',append=false,includes=fieldnotes.*')
    run(args + ['-cp', os.pathsep.join([str(CLASSES), str(LIBRARY)]), 'fieldnotes.cli.Main'])


def cobertura(source, destination):
    report = ET.Element('coverage', {'version': 'jacoco-conversion', 'lines-covered': '0', 'lines-valid': '0'})
    packages = ET.SubElement(report, 'packages')
    covered = total = 0
    for package in ET.parse(source).getroot().findall('package'):
        output_package = ET.SubElement(packages, 'package', {'name': package.attrib['name']})
        classes = ET.SubElement(output_package, 'classes')
        for file in package.findall('sourcefile'):
            path = LANE / 'src' / package.attrib['name'] / file.attrib['name']
            cls = ET.SubElement(classes, 'class', {'name': file.attrib['name'], 'filename': path.relative_to(ROOT).as_posix()})
            lines = ET.SubElement(cls, 'lines')
            for line in file.findall('line'):
                hit = int(line.attrib['ci']) > 0
                ET.SubElement(lines, 'line', {'number': line.attrib['nr'], 'hits': str(int(hit))})
                total += 1
                covered += int(hit)
    if not total:
        raise SystemExit('JaCoCo report has no executable lines')
    report.set('lines-covered', str(covered))
    report.set('lines-valid', str(total))
    report.set('line-rate', str(covered / total))
    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(report).write(destination, encoding='utf-8', xml_declaration=True)


def main():
    command = sys.argv[1] if len(sys.argv) == 2 else ''
    if command == 'setup':
        CACHE.mkdir(parents=True, exist_ok=True)
        for tool in TOOLS:
            target = CACHE / tool['file']
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() == tool['sha256']:
                continue
            data = urllib.request.urlopen(tool['url'], timeout=60).read()
            if hashlib.sha256(data).hexdigest() != tool['sha256']:
                raise SystemExit('Checksum mismatch: ' + tool['file'])
            target.write_bytes(data)
        tools_ready()
        return
    tools_ready()
    if command == 'build':
        compile_sources()
    elif command == 'lint':
        compile_sources(lint=True)
    elif command == 'run':
        compile_sources()
        application()
    elif command == 'architecture':
        compile_sources()
        output = run([JDEPS, '-verbose:class', '-filter:none', '--class-path', str(LIBRARY), str(CLASSES)], capture_output=True, text=True).stdout
        (CACHE / 'dependencies.txt').write_text(output)
        violations = [line for line in output.splitlines()
                      if re.search(r'fieldnotes\.domain\S*\s+->\s+fieldnotes\.cli', line)]
        if violations:
            raise SystemExit('Domain must not depend on CLI:\n' + '\n'.join(violations))
        if 'fieldnotes.domain.Transition' not in output:
            raise SystemExit('No domain bytecode found in dependency report')
        print('Scala architecture: domain does not depend on CLI')
    elif command == 'coverage':
        destination = Path(os.environ['POLYGLOT_COVERAGE_REPORT'])
        if not destination.is_absolute():
            raise SystemExit('POLYGLOT_COVERAGE_REPORT must be absolute')
        compile_sources()
        execution = CACHE / 'jacoco.exec'
        application(execution)
        xml = CACHE / 'jacoco.xml'
        run([JAVA, '-jar', str(CACHE / 'org.jacoco.cli-0.8.13-nodeps.jar'), 'report', str(execution),
             '--classfiles', str(CLASSES), '--sourcefiles', str(LANE / 'src'), '--xml', str(xml), '--quiet'], stdout=sys.stderr)
        cobertura(xml, destination)
    elif command == 'versions':
        run([JAVA, '-version'])
        print('Scala 2.13.16; WartRemover 3.3.4; JaCoCo 0.8.13')
    else:
        raise SystemExit('Usage: check.sh setup|build|lint|run|coverage|architecture|versions')


if __name__ == '__main__':
    main()
