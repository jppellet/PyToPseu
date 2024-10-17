import ast
import os
from os import path
from typing import NamedTuple

# See https://docs.python.org/3/library/ast.html#module-ast


def unparsed(expr: ast.AST) -> str:
    return ast.unparse(expr)


def readable_type(expr: ast.expr) -> str:
    s = ast.unparse(expr)
    match s:
        case "int":
            return "un nombre entier"
        case "float":
            return "un nombre à virgule"
        case "str":
            return "une chaîne de caractères"
        case "bool":
            return "une valeur booléenne"
        case _:
            return s


def readable_func(expr: str) -> str:
    match expr:
        case "math.sqrt":
            return "la racine carrée de "
        case "abs":
            return "la valeur absolue de "
        case "type":
            return "le type de "
        case "len":
            return "la longueur de "
        case "print":
            return "affiche "
        case _:
            return f"appelle la fonction {expr} "


def compop(op: ast.cmpop) -> str:
    match op:
        case ast.Eq():
            return "est égal à"
        case ast.NotEq():
            return "est différent de"
        case ast.Lt():
            return "est plus petit que"
        case ast.LtE():
            return "est plus petit que ou égal à"
        case ast.Gt():
            return "est plus grand que"
        case ast.GtE():
            return "est plus grand que ou égal à"
        case ast.Is():
            return "est"
        case ast.IsNot():
            return "n'est pas"
        case ast.In():
            return "est dans"
        case ast.NotIn():
            return "n'est pas dans"
        case _:
            print(f"WARNING Unknown comparison operator: {type(op).__name__}")
            return ast.unparse(op)


class OutStr(NamedTuple):
    line: int
    indent: int
    str: str


class Analyzer(ast.NodeVisitor):
    def __init__(self, use_markdown: bool) -> None:
        self.use_markdown = use_markdown
        self._out_buffer: list[OutStr] = []
        self._indent: int = 0
        self._stack: list[ast.AST] = []

    def indent(self) -> None:
        self._indent += 1

    def outdent(self) -> None:
        self._indent -= 1

    def append(self, node: ast.stmt | ast.expr, str: str, linedelta: int = 0) -> None:
        self._out_buffer.append(OutStr(node.lineno + linedelta, self._indent, str))

    def visit(self, node: ast.AST | None) -> None:
        if node is None:
            return
        self._stack.append(node)
        try:
            super().visit(node)
        finally:
            self._stack.pop()

    def generic_visit(self, node: ast.AST) -> None:
        print(f"ERROR Unhandled AST node: {type(node).__name__}")
        print(unparsed(node))

    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_Import(self, node: ast.Import) -> None:
        imports = [f"`{alias.name}`" for alias in node.names]
        what = "les modules" if len(imports) > 1 else "le module"
        self.append(node, f"on va utiliser {what} {', '.join(imports)}")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module
        imports = [
            f"`{alias.name}`{f" (en l'appelant `{alias.asname}`)" if alias.asname else ""}"
            for alias in node.names
        ]
        what = "les éléments" if len(imports) > 1 else "l'élément"
        self.append(node, f"on va utiliser {what} {', '.join(imports)} du module `{module}`")

    def visit_Expr(self, node: ast.Expr) -> None:
        self.visit(node.value)

    def visit_Assign(self, node: ast.Assign) -> None:
        # detect incrementation
        match node.value:
            case ast.BinOp(left=ast.Name(), right=ast.Constant(), op=ast.Add()):
                self.append(node, f"ajoute ")
                self.visit(node.value.right)
                self.append(node, f" à `{unparsed(node.targets[0])}`")
            case ast.BinOp(left=ast.Name(), right=ast.Constant(), op=ast.Sub()):
                self.append(
                    node,
                    f"diminue `{unparsed(node.targets[0])}` de ",
                )
                self.visit(node.value.right)
            case _:
                self.append(node, f"dans `{unparsed(node.targets[0])}`, stocke ")
                self.visit(node.value)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.append(
            node,
            f"dans `{unparsed(node.target)}`, prévu pour {readable_type(node.annotation)}, stocke ",
        )
        self.visit(node.value)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        var = unparsed(node.target)
        match node.op:
            case ast.Add():
                self.append(node, f"ajoute ")
                self.visit(node.value)
                self.append(node, f" à `{var}`")
            case ast.Sub():
                self.append(node, f"diminue `{var}` de ")
                self.visit(node.value)
            case ast.Mult():
                self.append(node, f"multiplie `{var}` par ")
                self.visit(node.value)
            case ast.Div():
                self.append(node, f"divise `{var}` par ")
                self.visit(node.value)
            case ast.FloorDiv():
                self.append(node, f"divise en nombres entiers `{var}` par ")
                self.visit(node.value)
            case ast.Mod():
                self.append(node, f"dans `{var}`, stocke le reste de la division de `{var}` par ")
                self.visit(node.value)
            case ast.Pow():
                self.append(node, f"dans `{var}`, stocke `{var}` à la puissance ")
                self.visit(node.value)
            case _:
                self.append(node, f"dans `{var}`, stocke le résultat de `{var}` {node.op} ")
                self.visit(node.value)

    def visit_Constant(self, node: ast.Constant) -> None:
        if isinstance(node.value, str):
            if len(node.value) == 0:
                self.append(node, "une chaîne de caractères vide")
            else:
                self.append(node, f'"{node.value}"')
        else:
            self.append(node, f"{node.value}")

    def visit_BinOp(self, node: ast.BinOp) -> None:
        match node.op:
            case ast.Add():
                self.append(node, "la somme de ")
                self.visit(node.left)
                self.append(node, f" et ")
                self.visit(node.right)
            case ast.Sub():
                self.append(node, "la différence entre ")
                self.visit(node.left)
                self.append(node, f" et ")
                self.visit(node.right)
            case ast.Mult():
                self.append(node, "le produit ")
                self.visit(node.left)
                self.append(node, f" × ")
                self.visit(node.right)
            case ast.Div():
                self.append(node, "le quotient de ")
                self.visit(node.left)
                self.append(node, f" divisé par ")
                self.visit(node.right)
            case ast.FloorDiv():
                self.append(node, "le quotient entier de ")
                self.visit(node.left)
                self.append(node, f" divisé par ")
                self.visit(node.right)
            case ast.Mod():
                self.append(node, "le reste de la division de ")
                self.visit(node.left)
                self.append(node, f" par ")
                self.visit(node.right)
            case ast.Pow():
                self.visit(node.left)
                self.append(node, f" à la puissance ")
                self.visit(node.right)
            case _:
                self.append(node, "le résultat de ")
                self.visit(node.left)
                self.append(node, f" {node.op} ")
                self.visit(node.right)

    def visit_Call(self, node: ast.Call) -> None:
        self.append(node, readable_func(unparsed(node.func)))
        for arg in node.args:
            self.visit(arg)

    def visit_Name(self, node: ast.Name) -> None:
        self.append(node, f"`{node.id}`")

    def visit_For(self, node: ast.For) -> None:
        # loop variable
        loop_var = unparsed(node.target)
        match node.iter:
            case ast.Call(
                func=ast.Name(id="range"),
                args=[to]
                | [ast.Constant(value=0), ast.Constant() as to]
                | [ast.Constant(value=0), ast.Constant() as to, ast.Constant(value=1)],
            ):
                is_to_constant = isinstance(to, ast.Constant)
                self.append(node, f"répète {"" if is_to_constant else "⟨"}")
                with_loop_var = "" if loop_var == "_" else f" (en comptant avec `{loop_var}` depuis 0)"
                self.visit(to)
                self.append(node, f"{"" if is_to_constant else "⟩"} fois{with_loop_var}:")
            case ast.Constant(value=str(value)):
                with_loop_var = "" if loop_var == "_" else f" (qu'on va appeler `{loop_var}`)"
                self.append(node, f'pour chaque caractère dans "{value}"{with_loop_var}:')
            case _:
                self.append(node, "pour chaque élément de ")
                self.visit(node.iter)
                with_loop_var = "" if loop_var == "_" else f" (qu'on va appeler `{loop_var}`)"
                self.append(node, f"{with_loop_var}:")

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()

    def visit_While(self, node: ast.While) -> None:
        self.append(node, "tant que ")
        self.visit(node.test)
        self.append(node, ":")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()

    def visit_Subscript(self, node: ast.Subscript) -> None:
        match node.slice:
            case ast.Slice(lower, upper, step):
                lower_is_none_or_zero = (
                    lower is None or isinstance(lower, ast.Constant) and lower.value in (None, 0)
                )
                upper_is_none_or_end = upper is None or unparsed(upper) == f"len({unparsed(node.value)})"
                step_none_or_one = step is None or isinstance(step, ast.Constant) and step.value in (None, 1)
                if lower_is_none_or_zero:
                    if upper_is_none_or_end:
                        self.append(node, "une copie de ")
                        self.visit(node.value)
                    else:
                        # upper is given
                        self.append(node, "les ")
                        self.visit(upper)
                        self.append(node, " premiers éléments de ")
                        self.visit(node.value)
                else:
                    # lower is given
                    if upper_is_none_or_end:
                        self.append(node, "les éléments de ")
                        self.visit(node.value)
                        self.append(node, " à partir de la position ")
                        self.visit(lower)
                    else:
                        # upper is given
                        self.append(node, f"les éléments de ")
                        self.visit(node.value)
                        self.append(node, f" de la position ")
                        self.visit(lower)
                        self.append(node, f" à ")
                        self.visit(upper)

                if not step_none_or_one:
                    self.append(node, f" avec un élément sur {step}")

            case ast.Name(id) if len(id) == 1:
                self.append(node, f"le {id}ᵉ élément de ")
                self.visit(node.value)
            case index:
                self.append(node, "l'élément ")
                self.visit(index)
                self.append(node, " de ")
                self.visit(node.value)

    def visit_If(self, node: ast.If) -> None:
        self.append(node, "si ")
        self.visit(node.test)
        self.append(node, ":")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.orelse:
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                # elif
                self.append(node.orelse[0], "sinon, ")
                self.visit(node.orelse[0])
            else:
                self.append(node.orelse[0], "sinon:", linedelta=-1)
                self.indent()
                for stmt in node.orelse:
                    self.visit(stmt)
                self.outdent()

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        first_level_condition = isinstance(self._stack[-2], (ast.If, ast.While))
        suffix = "" if not first_level_condition else " que"
        op_str = (
            "et" if isinstance(node.op, ast.And) else "ou" if isinstance(node.op, ast.Or) else "???"
        ) + suffix
        for i, value in enumerate(node.values):
            if i > 0:
                self.append(node, f" {op_str} ")
            self.visit(value)

    def visit_Compare(self, node: ast.Compare) -> None:
        # match  something like x % 2 == 0
        match node:
            case ast.Compare(
                left=ast.BinOp(left=left, right=ast.Constant(value), op=ast.Mod()),
                ops=[(ast.Eq() | ast.NotEq()) as eq_neq],
                comparators=[ast.Constant(value=0)],
            ):
                self.visit(left)
                is_eq = isinstance(eq_neq, ast.Eq)
                match (is_eq, value):
                    case (True, 2):
                        self.append(node, " est un nombre pair")
                    case (False, 2):
                        self.append(node, " est un nombre impair")
                    case (True, _):
                        self.append(node, f" est un multiple de {value}")
                    case (False, _):
                        self.append(node, f" n'est pas un multiple de {value}")
            case ast.Compare(
                left,
                ops=[op],
                comparators=[right],
            ):
                is_in = isinstance(op, ast.In)
                is_not_in = isinstance(op, ast.NotIn)
                # reverse for legibility
                if is_in or is_not_in:
                    self.visit(right)
                    self.append(node, " contient " if is_in else " ne contient pas ")
                    self.visit(left)
                else:
                    self.visit(left)
                    self.append(node, f" {compop(op)} ")
                    self.visit(right)
            case _:
                self.visit(node.left)
                for op, comp in zip(node.ops, node.comparators):
                    self.append(node, f" {op} ")
                    self.visit(comp)


def annotate(file: str, use_markdown: bool) -> None:
    print(f"Processing '{file}'")
    source = ""
    with open(file, "r", encoding="utf8") as source_file:
        source = source_file.read()
        tree = ast.parse(source, type_comments=True)

    analyzer = Analyzer(use_markdown)
    analyzer.visit(tree)

    num_lines = max(map(lambda x: x.line, analyzer._out_buffer))
    lines: list[str] = [""] * (num_lines + 1)
    for outstr in analyzer._out_buffer:
        line = outstr.line
        use_indent = not bool(lines[line])
        indent = "|   " * outstr.indent if use_indent else ""
        lines[line] += f"{indent}{outstr.str}"

    lines = lines[1:]  # skip first empty line
    src_lines = source.split("\n")
    max_src_width = max(map(len, src_lines)) + 2
    margin_width = 3
    margin = " " * margin_width

    format_code_line = (
        (lambda src: "`" + src + "`" if src else "&nbsp;" if use_markdown else "")
        if use_markdown
        else lambda src: src
    )

    outfile = path.splitext(file)[0] + (".md" if use_markdown else ".txt")
    with open(outfile, "w", encoding="utf8") as out_file:
        out_file.write(f"{"Source":{max_src_width}}{margin}|{margin}Pseudocode\n")
        out_file.write(
            "-" * (max_src_width + margin_width) + "|" + "-" * (max_src_width + margin_width) + "\n"
        )
        for src, pseu in zip(source.split("\n"), lines):
            out_file.write(f"{format_code_line(src):{max_src_width}}{margin}|{margin}{pseu}\n")

    print(f"Output written to '{outfile}'\n")


def annotate_all(use_markdown: bool) -> None:
    for file in sorted(os.listdir("sample_src")):
        if file.endswith(".py"):
            annotate(path.join("sample_src", file), use_markdown)


if __name__ == "__main__":
    use_markdown = False
    annotate_all(use_markdown)
    # annotate("sample_src/sample7.py", use_markdown)
