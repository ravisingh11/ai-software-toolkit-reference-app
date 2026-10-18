"""Check native jdeps output against an explicit domain dependency allowlist."""
from pathlib import Path
import sys

edges = []
for line in Path(sys.argv[1]).read_text().splitlines():
    parts = line.split()
    if len(parts) >= 3 and parts[1] == "->" and parts[0].startswith("fieldnotes.domain."):
        edges.append((parts[0], parts[2]))
if not edges:
    raise ValueError("jdeps produced no domain dependencies")
allowed = {"java.lang.Object", "java.lang.String", "java.util.Set"}
violations = [(src, target) for src, target in edges
              if target not in allowed and not target.startswith("fieldnotes.domain.")]
if violations:
    raise ValueError(f"Domain dependencies outside allowlist: {violations}")
print(f"Architecture: {len(edges)} domain dependency edges verified")
