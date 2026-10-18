"""Convert real JaCoCo executable-line counters to Cobertura line hits."""
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

source = ET.parse(sys.argv[1]).getroot()
output = Path(os.environ["POLYGLOT_COVERAGE_REPORT"])
if not output.is_absolute():
    raise ValueError("POLYGLOT_COVERAGE_REPORT must be absolute")
coverage = ET.Element("coverage")
packages = ET.SubElement(coverage, "packages")
package = ET.SubElement(packages, "package", name="fieldnotes.domain")
classes = ET.SubElement(package, "classes")
count = 0
for pkg in source.findall("package"):
    if pkg.get("name") != "fieldnotes/domain":
        continue
    for src in pkg.findall("sourcefile"):
        cls = ET.SubElement(classes, "class", name=src.attrib["name"],
                            filename="examples/polyglot/java/src/fieldnotes/domain/" + src.attrib["name"])
        lines = ET.SubElement(cls, "lines")
        for line in src.findall("line"):
            ET.SubElement(lines, "line", number=line.attrib["nr"],
                          hits="1" if int(line.attrib["ci"]) > 0 else "0")
            count += 1
if not count:
    raise ValueError("JaCoCo report contains no domain executable lines")
output.parent.mkdir(parents=True, exist_ok=True)
ET.ElementTree(coverage).write(output, encoding="utf-8", xml_declaration=True)
