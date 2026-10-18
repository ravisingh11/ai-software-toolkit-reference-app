"""Check this small domain's static Python AST, not arbitrary runtime imports."""
import ast
from pathlib import Path

source = Path(__file__).parent / "src/domain.py"
tree = ast.parse(source.read_text(), filename=str(source))
for node in ast.walk(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise SystemExit("Pure domain must not import CLI, I/O, or another module")
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {
        "__import__", "open", "eval", "exec", "input", "print"
    }:
        raise SystemExit("Pure domain must not perform dynamic imports or I/O")
print("Python architecture passed: pure domain has no imports or direct I/O")
