import ast
import os
from enum import Enum, auto
from os import path
from typing import NamedTuple


class Format(Enum):
    TEXT = auto()
    MARKDOWN = auto()
    PYTHON = auto()


# See https://docs.python.org/3/library/ast.html#module-ast

CURRENT_LINE = -1


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


HAS_LOWER_UNDERLINE = "gjpqy"


def fake_underline_helper(string: str, u: str) -> str:
    all_lower = all(c in HAS_LOWER_UNDERLINE for c in string)

    def subs(c: str) -> str:
        if c == "_":
            return " " + u
        if not all_lower and c in HAS_LOWER_UNDERLINE:
            return c
        return c + u

    return "".join(subs(c) for c in string)


def fake_underline(string: str) -> str:
    return fake_underline_helper(string, "\u0332")


def fake_double_underline(string: str) -> str:
    return fake_underline_helper(string, "\u0333")


def var(name: str) -> str:
    # return f"`{name}`" # markdown
    return fake_underline(name)  # text


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
            return "fait partie de"
        case ast.NotIn():
            return "ne fait pas partie de"
        case _:
            unhandled(f"comparison operator: {type(op).__name__}")
            return ast.unparse(op)


def unhandled(msg: str) -> None:
    print(f"ERROR Unhandled: {msg}")


class OutStr(NamedTuple):
    line: int
    indent: int
    str: str
    allow_break: bool


class Analyzer(ast.NodeVisitor):
    def __init__(self, format: Format) -> None:
        self.format = format
        self._out_buffer: list[OutStr] = []
        self._indent: int = 0
        self._stack: list[ast.AST] = []

    def indent(self) -> None:
        self._indent += 1

    def outdent(self) -> None:
        self._indent -= 1

    def append(
        self, node: ast.stmt | ast.expr | None, str: str, linedelta: int = 0, allow_break: bool = False
    ) -> None:
        line = CURRENT_LINE if node is None else node.lineno
        self._out_buffer.append(OutStr(line + linedelta, self._indent, str, allow_break))

    def visit(self, node: ast.AST | None, insert_brace_if_complex=False) -> None:
        if node is None:
            return
        self._stack.append(node)
        is_complex = False
        if insert_brace_if_complex and is_complex_node(node):
            self.append(None, "⟨")
            is_complex = True
        try:
            super().visit(node)
        finally:
            if is_complex:
                self.append(None, "⟩")
            self._stack.pop()

    def generic_visit(self, node: ast.AST) -> None:
        unhandled(f"AST node: {type(node).__name__}")
        print(unparsed(node))

    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            self.visit(stmt)

    def visit_Import(self, node: ast.Import) -> None:
        imports = [f"{var(alias.name)}" for alias in node.names]
        what = "les modules" if len(imports) > 1 else "le module"
        self.append(node, f"on va utiliser {what} {', '.join(imports)}")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module
        imports = [
            f"{var(alias.name)}{f" (en l'appelant {var(alias.asname)}" if alias.asname else ""}"
            for alias in node.names
        ]
        what = "les éléments" if len(imports) > 1 else "l'élément"
        self.append(node, f"on va utiliser {what} {', '.join(imports)} du module {var(module or '')}")

    def visit_Expr(self, node: ast.Expr) -> None:
        self.visit(node.value)

    def visit_Assign(self, node: ast.Assign) -> None:
        # detect incrementation
        if len(node.targets) == 1:
            target = unparsed(node.targets[0])
            match node.value:
                case ast.BinOp(ast.Name(src), ast.Add(), inc) | ast.BinOp(
                    inc, ast.Add(), ast.Name(src)
                ) if src == target:
                    self.append(node, f"ajoute ")
                    self.visit(inc)
                    self.append(node, f" à {var(target)}")
                case ast.BinOp(ast.Name(src), ast.Sub(), dec) if src == target:
                    self.append(node, f"diminue {var(target)} de ")
                    self.visit(dec)
                case ast.BinOp(ast.Name(src), ast.Mult(), mul) | ast.BinOp(
                    mul, ast.Mult(), ast.Name(src)
                ) if src == target:
                    self.append(node, f"multiplie {var(target)} par ")
                    self.visit(mul)
                case ast.BinOp(ast.Name(src), ast.Div() | ast.FloorDiv() as op, dec) if src == target:
                    self.append(node, f"divise {var(target)} par ")
                    self.visit(dec)
                    if isinstance(op, ast.FloorDiv):
                        self.append(node, " en nombres entiers")
                case _:
                    self.append(node, f"dans {var(target)}, stocke ")
                    self.visit(node.value)
        else:
            unhandled("multiple assignment")

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self.append(
            node,
            f"dans {var(unparsed(node.target))}, prévu pour {readable_type(node.annotation)}, stocke ",
        )
        self.visit(node.value)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        ident = unparsed(node.target)
        match node.op:
            case ast.Add():
                self.append(node, f"ajoute ")
                self.visit(node.value)
                self.append(node, f" à {var(ident)}")
            case ast.Sub():
                self.append(node, f"diminue {var(ident)} de ")
                self.visit(node.value)
            case ast.Mult():
                self.append(node, f"multiplie {var(ident)} par ")
                self.visit(node.value)
            case ast.Div():
                self.append(node, f"divise {var(ident)} par ")
                self.visit(node.value)
            case ast.FloorDiv():
                self.append(node, f"divise en nombres entiers {var(ident)} par ")
                self.visit(node.value)
            case ast.Mod():
                self.append(node, f"dans {var(ident)}, stocke le reste de la division de {var(ident)} par ")
                self.visit(node.value)
            case ast.Pow():
                self.append(node, f"dans {var(ident)}, stocke {var(ident)} à la puissance ")
                self.visit(node.value)
            case _:
                self.append(node, f"dans {var(ident)}, stocke le résultat de {var(ident)} {node.op} ")
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
        # detect modulo-zero checks
        match node:
            case ast.BinOp(left, ast.Mod(), ast.Constant(value)) if (
                n_digits := num_zeros_if_power_of_10(value)
            ) is not None:
                what = (
                    "le chiffre des unités de " if n_digits == 1 else f"les {n_digits} derniers chiffres de "
                )
                self.visit(left)
                self.append(node, f" modulo {value} (donc {what}")
                self.visit(left)
                self.append(node, f")")

            case _:
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
        funcname = unparsed(node.func)
        args = node.args
        match funcname:
            case "print":
                if len(args) == 0:
                    self.append(node, "affiche une ligne vide")
                else:
                    self.append(node, "affiche ")
                    for i, arg in enumerate(args):
                        if i > 0:
                            self.append(node, " et ")
                        self.visit(arg)

            case "math.sqrt":
                self.append(node, "la racine carrée de ")
                self.visit(args[0])
            case "abs":
                self.append(node, "la valeur absolue de ")
                self.visit(args[0])
            case "type":
                self.append(node, "le type de ")
                self.visit(args[0])
            case "len":
                self.append(node, "la longueur de ")
                self.visit(args[0])
            case "range":
                numargs = len(args)
                if numargs == 0:
                    self.append(node, f"une plage indéfinie")
                else:
                    from_: ast.expr | None = None
                    to: ast.expr | None = None
                    step: ast.expr | None = None
                    if numargs == 1:
                        from_ = ast.Constant(value=0, lineno=node.lineno, col_offset=node.col_offset)
                        to = args[0]
                    elif numargs == 2:
                        from_, to = args
                    elif numargs <= 3:
                        from_, to, step = args

                self.append(node, f"la plage de ")
                self.visit(from_, insert_brace_if_complex=True)
                self.append(node, f" à ")
                self.visit(to, insert_brace_if_complex=True)
                if step is not None and not (isinstance(step, ast.Constant) and step.value == 1):
                    self.append(node, f" avec un pas de ")
                    self.visit(step, insert_brace_if_complex=True)
            case _:
                self.append(node, f"appelle la fonction {funcname} ")
                for i, arg in enumerate(args):
                    if i > 0:
                        self.append(node, ", ")
                    self.visit(arg)

    def visit_Name(self, node: ast.Name) -> None:
        self.append(node, var(node.id))

    def visit_For(self, node: ast.For) -> None:
        # loop variable
        loop_var = unparsed(node.target)
        is_throwaway_var = loop_var == "_"
        match node.iter:

            # range(len(...))
            case ast.Call(ast.Name("range"), [ast.Call(ast.Name("len"), [iterable])]):
                self.append(node, f"répète autant de fois qu'il y a d'éléments dans ")
                self.visit(iterable, insert_brace_if_complex=True)
                if not is_throwaway_var:
                    self.append(node, f" (en comptant avec {var(loop_var)} depuis 0):", allow_break=True)
                else:
                    self.append(node, f":")

            # numerical range
            case ast.Call(
                ast.Name(id="range"),
                args=[to] | [ast.Constant(value=0), to] | [ast.Constant(value=0), to, ast.Constant(value=1)],
            ):
                with_loop_var = "" if is_throwaway_var else f" (en comptant avec {var(loop_var)} depuis 0)"

                self.append(node, f"répète ")
                self.visit(to, insert_brace_if_complex=True)
                self.append(node, f" fois{with_loop_var}:")

            case ast.Call(ast.Name("enumerate"), [iterable, *other_args]):
                self.append(node, "pour chaque élément de ")
                self.visit(iterable)
                if is_throwaway_var:
                    self.append(node, f":")
                else:
                    match node.target:
                        case ast.Tuple([ast.Name(index), ast.Name(elem)]):
                            self.append(
                                node,
                                f" (qu'on va appeler {var(elem)} et numéroter {var(index)} depuis ",
                                allow_break=True,
                            )
                            if len(other_args) == 1:
                                self.visit(other_args[0])
                            else:
                                self.append(node, "0")
                            self.append(node, "):")
                        case _:
                            # single loop variable
                            unhandled("single loop variable for enumerate")

            case ast.Constant(str(value)):
                with_loop_var = "" if is_throwaway_var else f" (qu'on va appeler {var(loop_var)})"
                self.append(node, f'pour chaque caractère dans "{value}"{with_loop_var}:')

            case _:
                self.append(node, "pour chaque élément de ")
                self.visit(node.iter)
                with_loop_var = "" if is_throwaway_var else f" (qu'on va appeler {var(loop_var)})"
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
                self.append(node, f"le {var(id)}ᵉ élément de ")
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
        match node:

            # modulo-zero checks
            case ast.Compare(
                left=ast.BinOp(left, ast.Mod(), ast.Constant(value)),
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

            # standard single-op comparisons
            case ast.Compare(left, [op], [right]):
                is_in = isinstance(op, ast.In)
                is_not_in = isinstance(op, ast.NotIn)
                # reverse for legibility
                # if is_in or is_not_in:
                #     self.visit(right)
                #     self.append(node, " contient " if is_in else " ne contient pas ")
                #     self.visit(left)
                # else:
                self.visit(left)
                self.append(node, f" {compop(op)} ")
                self.visit(right)
            case _:
                self.visit(node.left)
                for op, comp in zip(node.ops, node.comparators):
                    self.append(node, f" {op} ")
                    self.visit(comp)


def is_complex_node(node: ast.AST) -> bool:
    """
    Nodes that should be enclosed in ⟨⟩ in a pseudocode subexpression
    """
    return not isinstance(node, (ast.Constant, ast.Name))


def num_zeros_if_power_of_10(value: int) -> int | None:
    if value <= 1:
        return None
    n = 0
    while value % 10 == 0:
        value //= 10
        n += 1
    return n if value == 1 else None


def annotate(file: str, format: Format) -> None:
    print(f"Processing '{file}'")

    MAX_LINE_WIDTH = 80
    V_BAR = "│"
    PYTHON_ANN_SEP = "#" + V_BAR
    CONTINUATION_MARK = "└╴"

    source = ""
    with open(file, "r", encoding="utf8") as source_file:
        source = source_file.read()

    # Strip our own annotations if we find them
    def strip_ann(line: str) -> str | None:
        if CONTINUATION_MARK in line:
            return None
        return line.split(PYTHON_ANN_SEP, 1)[0].rstrip()

    src_lines = [line_ for line in source.split("\n") if (line_ := strip_ann(line)) is not None]
    if (
        len(src_lines) >= 4
        and src_lines[0].startswith('"""')
        and src_lines[3].startswith('"""')
        and src_lines[2].startswith("---")
        and src_lines[1].startswith("Source")
    ):
        src_lines = src_lines[4:]
    tree = ast.parse("\n".join(src_lines), type_comments=True)

    analyzer = Analyzer(format)
    analyzer.visit(tree)

    num_lines = max(map(lambda x: x.line, analyzer._out_buffer))
    lines: list[str] = [""] * (num_lines + 1)
    last_line = 0
    line_delta = 0
    for outstr in analyzer._out_buffer:
        if outstr.line == CURRENT_LINE:
            line = last_line
        else:
            line = outstr.line + line_delta
        line_width = len(lines[line])
        base_indent = (V_BAR + "   ") * outstr.indent
        if line_width + len(outstr.str) > MAX_LINE_WIDTH and outstr.allow_break:

            src_lines.insert(line, "")
            line += 1
            line_delta += 1
            lines.append("")
            indent = f"{base_indent}{V_BAR}     {CONTINUATION_MARK} "
            out = outstr.str.lstrip()
        else:
            use_indent = not bool(lines[line])
            indent = base_indent if use_indent else ""
            out = outstr.str
        lines[line] += f"{indent}{out}"
        last_line = line

    lines = lines[1:]  # skip first empty line
    max_src_width = max(map(len, src_lines)) + 2
    margin_left_width = 1
    margin_right_width = 4
    margin_left = " " * margin_left_width
    margin_right = " " * margin_right_width

    use_markdown = format == Format.MARKDOWN
    format_code_line = (
        (lambda src: "`" + src + "`" if src else "&nbsp;" if use_markdown else "")
        if use_markdown
        else lambda src: src
    )

    ext = {Format.TEXT: ".txt", Format.MARKDOWN: ".md", Format.PYTHON: "_ann.py"}[format]
    outfile = path.splitext(file)[0] + ext
    sep = PYTHON_ANN_SEP if format == Format.PYTHON else "|"
    header_sep = "" if format != Format.PYTHON else f"{'"""':{max_src_width}}{margin_left}{sep}\n"
    with open(outfile, "w", encoding="utf8") as out_file:
        out_file.write(header_sep)
        out_file.write(f"{"Source":{max_src_width}}{margin_left}{sep}{margin_right}Pseudocode\n")
        out_file.write(
            "-" * (max_src_width + margin_left_width)
            + sep
            + "-" * (max_src_width + margin_right_width)
            + "\n"
        )
        out_file.write(header_sep)
        for src, pseu in zip(src_lines, lines):
            out_file.write(f"{format_code_line(src):{max_src_width}}{margin_left}{sep}{margin_right}{pseu}\n")

    print(f"Output written to '{outfile}'\n")


def annotate_all(format: Format) -> None:
    for file in sorted(os.listdir("sample_src")):
        if file.endswith(".py") and not file.endswith("_ann.py"):
            annotate(path.join("sample_src", file), format)


if __name__ == "__main__":
    format = Format.PYTHON
    # annotate_all(format)
    annotate("sample_src/sample9.py", format)
