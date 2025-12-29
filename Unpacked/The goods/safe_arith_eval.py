
import ast, operator

ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv
}
ALLOWED_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}

def safe_eval_expr(expr: str):
    node = ast.parse(expr, mode="eval")
    return _eval_node(node.body)

def _eval_node(node):
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_BINOPS:
        return ALLOWED_BINOPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_UNARYOPS:
        return ALLOWED_UNARYOPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.Num):
        return int(node.n)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int,)):
        return int(node.value)
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Tuple) and len(node.elts) == 1:
        return _eval_node(node.elts[0])
    raise ValueError(f"Unsupported or unsafe expression: {ast.dump(node)}")
