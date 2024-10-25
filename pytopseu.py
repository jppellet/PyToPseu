import ast
import json
from enum import Enum
from pprint import pprint
from typing import Iterable, NamedTuple, TypeVar


class Format(Enum):
    TEXT = "txt"
    MARKDOWN = "md"
    PYTHON = "py"


# See https://docs.python.org/3/library/ast.html#module-ast

CURRENT_LINE = -1
ASTERISKS = ["*", "†", "‡", "§", "‖", "¶", "Δ", "◊"]

T = TypeVar("T")


def track_last(iterable: Iterable[T]) -> Iterable[tuple[T, bool]]:
    it = iter(iterable)
    prev = next(it)
    for current in it:
        yield prev, False
        prev = current
    yield prev, True


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
            return "une valeur vrai/faux"
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
    return fake_underline(name)


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


class NameType(Enum):
    MODULE = "mod"
    VAR = "var"
    FUNC = "func"
    CLASS = "class"
    VAR_FUNC_CLASS = "var/func/class"

    def __repr__(self) -> str:
        return self.name


# Keep in sync with TypeScript type declaration
class AnnotationResult(NamedTuple):
    input_had_preamble: bool
    input_continuations: list[int]
    output: list[str]
    output_continuations: list[int]


class Analyzer(ast.NodeVisitor):
    def __init__(self, format: Format) -> None:
        self.format = format
        self._out_buffer: list[OutStr] = []
        self._indent = 0
        self._stack: list[ast.AST] = []
        self._names: dict[str, NameType] = {}

    def indent(self) -> None:
        self._indent += 1

    def outdent(self) -> None:
        self._indent -= 1

    def append(
        self,
        node: ast.stmt | ast.expr | ast.arg | None,
        str: str,
        linedelta: int = 0,
        allow_break: bool = False,
    ) -> None:
        line = CURRENT_LINE if node is None else node.lineno
        self._out_buffer.append(OutStr(line + linedelta, self._indent, str, allow_break))

    A = TypeVar("A", bound=ast.expr | ast.stmt | ast.arg)

    def sep_join(self, items: Iterable[A], sep: str = ", ", last_sep: str = " et ") -> Iterable[A]:
        """
        Join items with separators, like "a, b et c"
        """
        it = iter(items)
        try:
            prev = next(it)
        except StopIteration:
            return
        yield prev
        try:
            prev = next(it)
        except StopIteration:
            return
        for current in it:
            self.append(prev, sep)
            yield prev
            prev = current
        self.append(prev, last_sep)
        yield prev

    def dump_names(self) -> None:
        names: dict[NameType, list[str]] = {t: [] for t in NameType}
        for name, t in self._names.items():
            names[t].append(name)
        for t, ns in names.items():
            if ns:
                print(f"{repr(t)}: {', '.join(ns)}")

    def visit(self, node: ast.AST | None, insert_brace_if_complex=False) -> None:
        if node is None:
            return
        self._stack.append(node)
        is_complex = False
        if insert_brace_if_complex and not is_simple_node(node):
            self.append(None, "⟨", allow_break=True)
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
        for alias in node.names:
            name = alias.asname or alias.name
            self.new_name(name, NameType.MODULE)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module
        imports = [
            f"{var(alias.name)}{f" (en l'appelant {var(alias.asname)})" if alias.asname else ""}"
            for alias in node.names
        ]
        what = "les éléments" if len(imports) > 1 else "l'élément"
        self.append(node, f"on va utiliser {what} {', '.join(imports)} du module {var(module or '')}")
        for alias in node.names:
            name = alias.asname or alias.name
            self.new_name(name, NameType.VAR_FUNC_CLASS)

    def visit_Expr(self, node: ast.Expr) -> None:
        # ast.Expr is an expr as a statement
        self.visit_stored(node.value)

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
                    self.visit_stored(node.value)
        else:
            unhandled("multiple assignment")

        for varname in node.targets:
            self.new_name(varname, NameType.VAR)

    def visit_stored(self, node: ast.expr) -> None:
        match node:
            case ast.Compare() | ast.BoolOp(ast.Or() | ast.And(), _):
                self.append(node, "vrai/faux selon si ")
                self.visit(node)
            case _:
                self.visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            self.append(
                node,
                f"on prépare {var(unparsed(node.target))} pour y stocker un {readable_type(node.annotation)}",
            )
        else:
            self.append(
                node, f"dans {var(unparsed(node.target))}, prévu pour {readable_type(node.annotation)},"
            )
            self.append(node, f" stocke ", allow_break=True)
            self.visit_stored(node.value)
        self.new_name(node.target, NameType.VAR)

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
                self.visit_stored(node.value)
        self.new_name(node.target, NameType.VAR)

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        self.append(node, f"l'expansion de {unparsed(node)[1:]}")

    def new_name(self, node: ast.expr | str, t: NameType) -> None:
        match node:
            case ast.Name(id) | str(id):
                self._names[id] = t
            case _:
                pass

    def name_is(self, name: str, t: NameType) -> bool:
        return self._names.get(name) == t

    def visit_Constant(self, node: ast.Constant) -> None:
        match node.value:
            case str(value):
                if len(value) == 0:
                    self.append(node, "une chaîne de caractères vide")
                else:
                    self.append(node, f'"{value}"')
            case x if x == Ellipsis:
                self.append(node, "quelque chose à définir")
            case x if x == None:
                self.append(node, "une valeur vide")
            case _:
                self.append(node, f"{node.value}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        match node.op:
            case ast.USub():
                self.append(node, "l'opposé de ")
                self.visit(node.operand)
            case ast.UAdd():
                # self.append(node, "le même que ")
                self.visit(node.operand)
            case ast.Not():
                self.append(node, "le contraire de ")
                self.visit(node.operand, insert_brace_if_complex=True)
            case _:
                unhandled(f"unary operator: {type(node.op).__name__}")

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
            case "math.ceil":
                self.append(node, "l’arrondi supérieur de ")
                self.visit(args[0])
            case "math.floor":
                self.append(node, "l’arrondi inférieur de ")
                self.visit(args[0])
            case "math.sin":
                self.append(node, "le sinus de ")
                self.visit(args[0])
            case "math.cos":
                self.append(node, "le cosinus de ")
                self.visit(args[0])
            case "math.tan":
                self.append(node, "la tangente de ")
                self.visit(args[0])
            case "round":
                self.append(node, "l’arrondi de ")
                self.visit(args[0])
            case "input":
                if args:
                    self.append(node, "la réponse de l'utilisateur à la question ")
                    self.visit(args[0])
                else:
                    self.append(node, "ce que l'utilisateur va taper")
            case "str":
                self.append(node, "la conversion en chaîne de caractères de ")
                self.visit(args[0])
            case "float":
                self.append(node, "la conversion en nombre à virgule de ")
                self.visit(args[0])
            case "int":
                self.append(node, "la conversion en nombre entier de ")
                self.visit(args[0])
            case "bool":
                self.append(node, "la conversion en vrai/faux de ")
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

                def append_args(first_prefix: str = "avec ") -> None:
                    for i, arg in enumerate(args):
                        if i > 0:
                            self.append(node, ", ")
                        elif first_prefix:
                            self.append(node, first_prefix)
                        self.visit(arg)

                match node.func:
                    case ast.Attribute(expr, method):

                        def append_expr():
                            self.visit(expr, insert_brace_if_complex=True)

                        match method:
                            case "startswith":
                                append_expr()
                                self.append(node, f" commence par ")
                                append_args(first_prefix="")
                            case "endswith":
                                append_expr()
                                self.append(node, f" finit par ")
                                append_args(first_prefix="")
                            case "upper":
                                self.append(node, f"une copie tout en majuscules de ")
                                append_expr()
                            case "lower":
                                self.append(node, f"une copie tout en minuscules de ")
                                append_expr()
                            case "capitalize":
                                self.append(node, f"une copie avec la première lettre en majuscule de ")
                                append_expr()
                            case "title":
                                self.append(
                                    node,
                                    f"une copie avec la première lettre de chaque mot en majuscule de ",
                                )
                                append_expr()
                            case "strip":
                                self.append(node, f"une copie sans espaces de début et de fin de ")
                                append_expr()
                            case "lstrip":
                                self.append(node, f"une copie sans espaces de début de ")
                                append_expr()
                            case "rstrip":
                                self.append(node, f"une copie sans espaces de fin de ")
                                append_expr()
                            case _:
                                self.append(node, f"le résultat de la méthode {var(method)} de ")
                                append_expr()
                                append_args()
                    case _:
                        self.append(node, f"le résultat de la fonction {funcname} ")
                        append_args()

    def visit_Name(self, node: ast.Name) -> None:
        self.append(node, var(node.id))

    def visit_List(self, node: ast.List) -> None:
        num_elems = len(node.elts)
        if num_elems == 0:
            self.append(node, "une liste vide")
        elif num_elems == 1:
            self.append(node, "une liste avec un seul élément, ")
            self.visit(node.elts[0])
        else:
            self.append(node, f"une liste avec {num_elems} éléments: ")
            for elem in self.sep_join(node.elts):
                self.visit(elem)

    def visit_Pass(self, node: ast.Pass) -> None:
        self.append(node, "ne fais rien de spécial")

    def visit_Break(self, node: ast.Break) -> None:
        self.append(node, "interromps la boucle")

    def visit_Continue(self, node: ast.Continue) -> None:
        self.append(node, "passe à l'itération suivante")

    def visit_Return(self, node: ast.Return) -> None:
        if node.value is None:
            self.append(node, "sors de la fonction")
        else:
            self.append(node, "sors de la fonction en renvoyant ")
            self.visit(node.value)

    def visit_Yield(self, node: ast.Yield) -> None:
        if node.value is None:
            self.append(node, "génère une valeur vide")
        else:
            self.append(node, "génère ")
            self.visit(node.value)

    def visit_Try(self, node: ast.Try) -> None:
        self.append(node, "essaie ceci:")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.handlers:
            for handler in node.handlers:
                self.append(handler.body[0], "en cas d'erreur:", linedelta=-1)
                # TODO: de type blabla
                self.indent()
                for stmt in handler.body:
                    self.visit(stmt)
                self.outdent()
        if node.finalbody:
            self.append(node.finalbody[0], "dans tous les cas, finis par:", linedelta=-1)
            self.indent()
            for stmt in node.finalbody:
                self.visit(stmt)
            self.outdent()
        if node.orelse:
            self.append(node, "s'il n'y a pas eu d'erreur:", linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_Await(self, node: ast.Await) -> None:
        self.append(node, "attends ")
        self.visit(node.value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.append(node, f"définis la fonction {var(node.name)}, ")
        for arg in node.args.args:
            self.new_name(arg.arg, NameType.VAR)
        num_args = len(node.args.args)
        needs_and = num_args > 0

        def append_arg(arg: ast.arg) -> None:
            self.append(arg, var(arg.arg), allow_break=True)
            if arg.annotation:
                self.append(arg, " (")
                self.append(arg, readable_type(arg.annotation))
                self.append(arg, ")")

        if num_args == 0:
            self.append(node, "sans argument, ")
        elif num_args == 1:
            self.append(node, f"qui prend un argument, {var(node.args.args[0].arg)}, ")
        else:
            self.append(node, f"qui prend {num_args} arguments")
            for arg, is_last in track_last(node.args.args):
                if not is_last:
                    self.append(node, ", ")
                    append_arg(arg)
                else:
                    self.append(node, " et ")
                    append_arg(arg)
                    self.append(node, ", ")
        if node.returns:
            if needs_and:
                self.append(node, "et ")
            match node.returns:
                case ast.Constant(None):
                    self.append(node, "qui ne renvoie rien, ", allow_break=True)
                case _:
                    self.append(node, f"qui renvoie {readable_type(node.returns)}, ", allow_break=True)
        self.append(node, "ainsi:")

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()

    def visit_Lambda(self, node: ast.Lambda) -> None:

        self.append(node, "une fonction anonyme")
        for arg in node.args.args:
            self.new_name(arg.arg, NameType.VAR)
        num_args = len(node.args.args)
        if num_args == 0:
            self.append(node, " sans argument")
        elif num_args == 1:
            self.append(node, f" qui prend un argument, {var(node.args.args[0].arg)}, et")
        else:
            self.append(node, f" qui prend {num_args} arguments")
            for arg, is_last in track_last(node.args.args):
                if not is_last:
                    self.append(node, f", {var(arg.arg)}")
                else:
                    self.append(node, f" et {var(arg.arg)}, et")
        self.append(node, " qui renvoie ", allow_break=True)
        self.visit(node.body)

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
        if node.orelse:
            self.append(node.orelse[0], "si la boucle n'a pas été interrompue:", linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_While(self, node: ast.While) -> None:
        match node.test:
            case ast.Constant(True | 1):
                self.append(node, "répéter indéfiniment:")
            case _:
                self.append(node, "tant que ")
                self.visit_cond(node.test)
                self.append(node, ":")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        # TODO orelse part

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
                        self.visit(upper, insert_brace_if_complex=True)
                        self.append(node, " premiers éléments de ")
                        self.visit(node.value)
                else:
                    # lower is given
                    if upper_is_none_or_end:
                        self.append(node, "les éléments de ")
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, " à partir de la position ")
                        self.visit(lower, insert_brace_if_complex=True)
                    else:
                        # upper is given
                        self.append(node, f"les éléments de ")
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, f" de la position ")
                        self.visit(lower, insert_brace_if_complex=True)
                        self.append(node, f" à ")
                        self.visit(upper, insert_brace_if_complex=True)

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
        self.visit_cond(node.test)
        self.append(node, ":")
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.orelse:
            if (
                len(node.orelse) == 1
                and isinstance(node.orelse[0], ast.If)
                and node.orelse[0].col_offset == node.col_offset
            ):
                # elif
                self.append(node.orelse[0], "sinon, ")
                self.visit(node.orelse[0])
            else:
                self.append(node.orelse[0], "sinon:", linedelta=-1)
                self.indent()
                for stmt in node.orelse:
                    self.visit(stmt)
                self.outdent()

    def visit_cond(self, node: ast.expr) -> None:
        match node:
            case ast.Compare() | ast.BoolOp():
                self.visit(node)
            case ast.UnaryOp(ast.Not(), expr):
                self.visit(expr, insert_brace_if_complex=True)
                self.append(node, " est faux")
            case ast.Name():
                self.visit(node, insert_brace_if_complex=True)
                self.append(node, " est vrai")
            case _:
                self.visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        first_level_condition = isinstance(self._stack[-2], (ast.If, ast.While))
        suffix = "" if not first_level_condition else " que"
        op_str = (
            "et" if isinstance(node.op, ast.And) else "ou" if isinstance(node.op, ast.Or) else "???"
        ) + suffix
        for i, value in enumerate(node.values):
            if i > 0:
                self.append(node, f" {op_str} ")
            self.visit_cond(value)

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

            # Boolean checks
            case ast.Compare(ast.Constant(True), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, " est vrai")
            case ast.Compare(ast.Constant(False), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, " est faux")
            case ast.Compare(ast.Constant(True), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, " n'est pas vrai")
            case ast.Compare(ast.Constant(False), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, " n'est pas faux")

            # None checks
            case ast.Compare(ast.Constant(None), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, " est vide")

            case ast.Compare(ast.Constant(None), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, " n'est pas vide")

            # standard single-op comparisons
            case ast.Compare(left, [op], [right]):
                # is_in = isinstance(op, ast.In)
                # is_not_in = isinstance(op, ast.NotIn)
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


def is_simple_node(node: ast.AST) -> bool:
    """
    Nodes that should not be enclosed in ⟨⟩ in a pseudocode subexpression
    """
    return isinstance(node, (ast.Constant, ast.Name, ast.Subscript))


def num_zeros_if_power_of_10(value: int) -> int | None:
    if value <= 1:
        return None
    n = 0
    while value % 10 == 0:
        value //= 10
        n += 1
    return n if value == 1 else None


def frenchify(s: str) -> str:
    return (
        s.replace(" de les ", " des ")
        .replace(" de le ", " du ")
        .replace(" à le ", " au ")
        .replace(" à les ", " aux ")
    )


def annotate_file(file: str, format: Format, dump_ast: bool = False) -> None:
    print(f"Processing '{file}'")

    with open(file, "r", encoding="utf8") as source_file:
        source = source_file.read()

    annotated = annotate_code(source, format, dump_ast)
    if not annotated:
        print("Syntax error")
        return

    ext = {Format.TEXT: ".txt", Format.MARKDOWN: ".md", Format.PYTHON: "_ann.py"}[format]
    outfile = os.path.splitext(file)[0] + ext

    with open(outfile, "w", encoding="utf8") as out_file:
        out_file.write("\n".join(annotated.output))

    print(f"Output written to '{outfile}'\n")


def annotate_code(source: str, format: Format, dump_ast: bool = False) -> AnnotationResult | None:

    MAX_LINE_WIDTH = 60
    V_BAR = "│"
    PYTHON_ANN_SEP = "#" + V_BAR
    CONTINUATION_MARK = "└╴"
    PREAMBLE_LENGTH = 4
    MIN_CODE_WIDTH = 25
    LEFT_COL_HEADER = "Code"
    RIGHT_COL_HEADER = "Interprétation"

    input_continuations: list[int] = []

    # Strip our own annotations if we find them
    def strip_ann(line: str, number: int) -> str | None:
        if CONTINUATION_MARK in line:
            input_continuations.append(number)
            return None
        return line.split(PYTHON_ANN_SEP, 1)[0].rstrip()

    src_lines = [
        line_ for n, line in enumerate(source.split("\n"), 1) if (line_ := strip_ann(line, n)) is not None
    ]
    input_had_preamble = False
    if (
        len(src_lines) >= PREAMBLE_LENGTH
        and src_lines[0].startswith('"""')
        and src_lines[PREAMBLE_LENGTH - 1].startswith('"""')
        and src_lines[2].startswith("———")
        and src_lines[1].startswith(LEFT_COL_HEADER)
    ):
        input_had_preamble = True
        src_lines = src_lines[4:]

    try:
        tree = ast.parse("\n".join(src_lines), type_comments=True)
    except SyntaxError as e:
        return None

    if dump_ast:
        print(ast.dump(tree, indent=4))

    analyzer = Analyzer(format)
    analyzer.visit(tree)

    if dump_ast:
        analyzer.dump_names()

    lines: list[str] = [""] * (len(src_lines) + 1)
    last_line = 0
    output_continuations: list[int] = []
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
            output_continuations.append(PREAMBLE_LENGTH + line)
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
    max_src_width = max(MIN_CODE_WIDTH, max(map(len, src_lines))) + 2
    margin_left_width = 1
    margin_right_width = 3
    margin_left = " " * margin_left_width
    margin_right = " " * margin_right_width

    use_markdown = format == Format.MARKDOWN
    format_code_line = (
        (lambda src: "`" + src + "`" if src else "&nbsp;" if use_markdown else "")
        if use_markdown
        else lambda src: src
    )

    sep = PYTHON_ANN_SEP if format == Format.PYTHON else "|"
    header_sep = "" if format != Format.PYTHON else f"{'"""':{max_src_width}}{margin_left}{sep}"

    output_lines: list[str] = []

    output_lines.append('"""')
    output_lines.append(
        f"{LEFT_COL_HEADER:{max_src_width+1}}{margin_left}{sep[-1]}{margin_right}{RIGHT_COL_HEADER}"
    )
    output_lines.append(
        "—" * (max_src_width + max_src_width + margin_left_width + margin_right_width + len(sep))
    )
    output_lines.append(header_sep)
    last_index = len(src_lines) - 1
    for i, (src, pseu) in enumerate(zip(src_lines, lines)):
        pseu = frenchify(pseu)
        code_line = format_code_line(src)
        if i == last_index and len(code_line.strip()) == 0:
            # keep last line without annotation if empty, reduces glitches in editor
            output_lines.append(code_line)
        else:
            output_lines.append(f"{code_line:{max_src_width}}{margin_left}{sep}{margin_right}{pseu}")

    return AnnotationResult(input_had_preamble, input_continuations, output_lines, output_continuations)


def annotate_all(format: Format) -> None:
    for file in sorted(os.listdir("sample_src")):
        if file.endswith(".py") and not file.endswith("_ann.py"):
            annotate_file(os.path.join("sample_src", file), format)


result_json: str | None = None
if __name__ == "__main__":
    # check if local var __user_code__ exists
    format = Format.PYTHON

    local_vars = locals()
    ran_user_code = False
    if "__user_code__" in local_vars:
        code = local_vars["__user_code__"]
        if isinstance(code, str):
            ran_user_code = True
            result = annotate_code(code, format)
            if result:
                result_json = json.dumps(result._asdict())
            else:
                # syntax error
                pass

    if not ran_user_code:
        import os

        annotate_all(format)
        # annotate_file("sample_src/lectures_1to5.py", format)
        # annotate_file("sample_src/sample9.py", format)
        # annotate_file("sample_src/tmp.py", format, dump_ast=True)

result_json
