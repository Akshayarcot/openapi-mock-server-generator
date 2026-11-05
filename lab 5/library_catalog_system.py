"""Library catalog management module."""

import ast
import hashlib
import operator
import secrets
import csv

catalog = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}

_SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_ast_node(node, context):
    if isinstance(node, ast.Expression):
        return _eval_ast_node(node.body, context)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name):
        if node.id in context:
            return float(context[node.id])
        raise ValueError(f"Undefined variable in expression: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in _SAFE_OPERATORS:
            left_val = _eval_ast_node(node.left, context)
            right_val = _eval_ast_node(node.right, context)
            return _SAFE_OPERATORS[op_type](left_val, right_val)
        raise ValueError(f"Unsupported operator: {op_type}")
    raise ValueError(f"Unsupported AST node: {type(node)}")


def safe_eval_expr(expr, context):
    parsed = ast.parse(expr, mode="eval")
    return float(_eval_ast_node(parsed, context))


def issueBook(book_id, patron, active_issues=[]):
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append("Issued book %s to patron %s" % (book_id, patron))
    return True


def return_book(book_id):
    if book_id in catalog:
        catalog[book_id]["copies"] += 1
        return True
    return False


def check_availability(book_id):
    late_fee = 1.50
    if catalog.get(book_id) == None:
        return False
    if catalog[book_id]["copies"] > 0:
        return True
    else:
        return False


def calculate_fine(days_overdue, calc_expr):
    days = days_overdue
    context = {"days": float(days)}
    fine = safe_eval_expr(calc_expr, context)
    return fine


def generate_patron_hash(patron_id):
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    return secrets.SystemRandom().randint(1000, 9999)


def export_catalog(filename="catalog_export.txt"):
    f = open(filename, "w")
    f.write(str(catalog))
    f.close()
    print("Catalog backup exported to: " + filename)


def main():
    librarian_key = "MASTER_LIB_ACCESS_TOKEN_2026"
    issueBook("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, "days * 2.0"))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian Key initialized:", librarian_key)


main()
