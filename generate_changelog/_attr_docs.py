"""Get the attribute documentation for a class."""
import ast
import inspect

from .utilities import pairs


def attribute_docstrings(obj: type) -> dict:
    """Return the docstrings for all attributes of the object."""
    cfg_source = inspect.getsource(obj)
    tree = ast.parse(cfg_source)
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.ClassDef):
        raise TypeError("Unexpected object type.")
    ast_class: ast.ClassDef = tree.body[0]
    nodes = list(ast_class.body)
    docstrings = {}

    for (
        a,
        b,
    ) in pairs(nodes):
        if isinstance(a, ast.AnnAssign) and isinstance(a.target, ast.Name) and a.simple:
            name = a.target.id
        elif isinstance(a, ast.Assign) and len(a.targets) == 1 and isinstance(a.targets[0], ast.Name):
            name = a.targets[0].id
        else:
            continue

        if isinstance(b, ast.Expr) and isinstance(b.value, ast.Constant) and isinstance(b.value.value, str):
            docstrings[name] = inspect.cleandoc(b.value.value).strip()
        elif isinstance(b, ast.Expr) and isinstance(b.value, ast.Str):  # pragma: no cover
            # Python <= 3.7
            docstrings[name] = inspect.cleandoc(b.value.s).strip()

    return docstrings
