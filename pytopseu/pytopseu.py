import ast
import json

from types import EllipsisType, NoneType
from typing import Callable, Iterable, Iterator, NamedTuple, Type

from typing_extensions import TypeIs

from .common import *
from .pseudocode_dictionary import PseudocodeDictionary

# See https://docs.python.org/3/library/ast.html#module-ast

CURRENT_LINE = -1
ASTERISKS = ["*", "†", "‡", "§", "‖", "¶", "Δ", "◊"]


def try_infer_type_of(expr: ast.expr) -> type | None:
    match expr:
        case ast.Constant(value):
            match value:
                case str():
                    return str
                case int():
                    return int
                case float():
                    return float
                case bool():
                    return bool
                case bytes():
                    return bytes
                case complex():
                    return complex
                case x if x == Ellipsis:
                    return EllipsisType
                case x if x == None:
                    return NoneType
                case _:
                    unhandled(f"constant value: {value}")
                    return None
        case ast.List() | ast.ListComp():
            return list
        case ast.Set() | ast.SetComp():
            return set
        case ast.Dict() | ast.DictComp():
            return dict
        case ast.Tuple():
            return tuple
        case ast.FormattedValue() | ast.JoinedStr():
            return str
        case ast.BoolOp() | ast.Compare():
            return bool  # really? could be other things
        case _:
            unhandled(f"expression: {type(expr).__name__}")
            return None

        # TO HANDLE:
        #  | NamedExpr(expr target, expr value)
        #  | BinOp(expr left, operator op, expr right)
        #  | UnaryOp(unaryop op, expr operand)
        #  | Lambda(arguments args, expr body)
        #  | IfExp(expr test, expr body, expr orelse)
        #  | GeneratorExp(expr elt, comprehension* generators)
        #  -- the grammar constrains where yield expressions can occur
        #  | Await(expr value)
        #  | Yield(expr? value)
        #  | YieldFrom(expr value)
        #  | Call(expr func, expr* args, keyword* keywords)
        #  -- the following expression can appear in assignment context
        #  | Attribute(expr value, identifier attr, expr_context ctx)
        #  | Subscript(expr value, expr slice, expr_context ctx)
        #  | Starred(expr value, expr_context ctx)
        #  | Name(identifier id, expr_context ctx)
        #  -- can appear only in Subscript
        #  | Slice(expr? lower, expr? upper, expr? step)


def track_last[T](iterable: Iterable[T]) -> Iterator[tuple[T, bool]]:
    it = iter(iterable)
    prev = next(it)
    for current in it:
        yield prev, False
        prev = current
    yield prev, True


def unparsed(expr: ast.AST) -> str:
    return ast.unparse(expr)


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


def unhandled(msg: str) -> None:
    print(f"ERROR Unhandled: {msg}")


class OutStr(NamedTuple):
    line: int
    indent: int
    str: str
    allow_break: bool


class Module(NamedTuple):
    pass


class Var(NamedTuple):
    type: ast.expr | None


class Func(NamedTuple):
    # args: list[ast.arg]
    # returns: ast.expr | None
    pass


class Class(NamedTuple):
    pass


class VarFuncClass(NamedTuple):
    pass


NameInfo = Module | Var | Func | Class | VarFuncClass


def name_matches[T: NameInfo](
    obj: NameInfo, cls: Type[T], pred: Callable[[T], bool] | None = None
) -> TypeIs[T]:
    return isinstance(obj, cls) and (pred is None or pred(obj))


a: NameInfo = Module()
if name_matches(a, Var, lambda v: v.type is not None):
    print(a)


# Keep in sync with TypeScript type declaration
class AnnotationResult(NamedTuple):
    input_had_preamble: bool
    input_continuations: list[int]
    output: list[str]
    output_continuations: list[int]


class Analyzer(ast.NodeVisitor):
    def __init__(
        self,
        format: PseudocodeFormat,
        pseudocode_dictionary: PseudocodeDictionary
    ) -> None:
        self.format = format
        self.pd = pseudocode_dictionary
        self._out_buffer: list[OutStr] = []
        self._indent = 0
        self._stack: list[ast.AST] = []
        self._names: dict[str, NameInfo] = {}
        self._allow_break_for_next = False

    def indent(self) -> None:
        self._indent += 1

    def outdent(self) -> None:
        self._indent -= 1

    def allow_break_for_next(self) -> None:
        self._allow_break_for_next = True

    def append(
        self,
        node: ast.stmt | ast.expr | ast.arg | None,
        msg: str,
        linedelta: int = 0,
        allow_break: bool = False,
    ) -> None:
        line = CURRENT_LINE if node is None else node.lineno
        allow_break = allow_break or self._allow_break_for_next
        self._allow_break_for_next = False
        self._out_buffer.append(OutStr(line + linedelta, self._indent, str(msg), allow_break))

    def sep_join[A: ast.expr | ast.stmt | ast.arg](
        self,
        items: Iterable[A],
        sep: str = ", ",
        last_sep: str | None = None
    ) -> Iterable[A]:
        """
        Join items with separators, like "a, b et c"
        """
        if last_sep is None:
            last_sep = self.pd._and_
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
        for name, t in self._names.items():
            print(f"{name}: {t}")

    def compop(self, op: ast.cmpop) -> str:
        def helper():
            match op:
                case ast.Eq():
                    return self.pd.is_equal_to
                case ast.NotEq():
                    return self.pd.is_different_from
                case ast.Lt():
                    return self.pd.is_smaller_than
                case ast.LtE():
                    return self.pd.is_smaller_than_or_equal_to
                case ast.Gt():
                    return self.pd.is_greater_than
                case ast.GtE():
                    return self.pd.is_greater_than_or_equal_to
                case ast.Is():
                    return self.pd.is_
                case ast.IsNot():
                    return self.pd.is_not
                case ast.In():
                    return self.pd.is_in
                case ast.NotIn():
                    return self.pd.is_not_in
                case _:
                    unhandled(f"comparison operator: {type(op).__name__}")
                    return ast.unparse(op)

        return str(helper())

    def readable_type(self, expr: ast.expr, plural: bool = False) -> str:

        def helper(expr: ast.expr, plural: bool) -> tuple[str, Type | None]:

            # normalize attribute access so that e.g. typing.List becomes just List
            match expr:
                case ast.Attribute(_, attr):
                    expr = ast.Name(attr)

            match expr:
                # simple types
                case ast.Name(simpletype):
                    match simpletype:
                        case "int":
                            return self.pd.an_int if not plural \
                                else self.pd.ints, int
                        case "float":
                            return self.pd.a_float if not plural \
                            else self.pd.floats, float
                        case "str":
                            return self.pd.a_str if not plural \
                            else self.pd.strs, str
                        case "bool":
                            return self.pd.a_bool if not plural \
                            else self.pd.bools, bool
                        case "list" | "List":
                            return self.pd.a_list if not plural \
                            else self.pd.lists, list
                        case "set" | "Set":
                            return self.pd.a_set if not plural \
                            else self.pd.sets, set
                        case "dict" | "Dict" | "defaultdict":
                            return self.pd.a_dict if not plural \
                            else self.pd.dicts, dict
                        case "tuple" | "Tuple":
                            return self.pd.a_tuple if not plural \
                            else self.pd.tuples, tuple
                        case _:
                            return simpletype, None

                # parameterized types
                case ast.Subscript(paramtype, typeparams):
                    basedesc, basetype = helper(paramtype, plural)
                    if basetype is list or basetype is set:
                        elem = self.readable_type(typeparams, plural=True)
                        return self.pd.list_or_set_of.format(cont=basedesc, elem=elem), basetype
                    if basetype is dict:
                        match typeparams:
                            case ast.Tuple([keytype, valuetype]):
                                return (
                                    self.pd.dict_of.format(
                                        cont=basedesc,
                                        key=self.readable_type(keytype, plural=True),
                                        value=self.readable_type(valuetype, plural=True),
                                    ),
                                    basetype,
                                )
                            case _:
                                return self.pd.dict_malformed.format(cont=basedesc), basetype
                    if basetype is tuple:
                        return (
                            self.pd.tuple_of.format(cont=basedesc, elem=self.readable_type(typeparams, plural=True)),
                            basetype,
                        )

                    return (
                        self.pd.container_of.format(cont=basedesc, elem=self.readable_type(typeparams, plural=True)),
                        basetype,
                    )

                # multiple type parameters
                case ast.Tuple(elts):
                    return ", ".join(self.readable_type(e, plural) for e in elts), None  # not tuple

            # all the rest
            unparsed = ast.unparse(expr)
            unhandled(f"type with AST of class {type(expr).__name__}, {unparsed}")
            return unparsed, None

        return str(helper(expr, plural)[0])

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
        what = str(
            self.pd.the_modules if len(imports) > 1
            else self.pd.the_module
        )
        self.append(node, self.pd.well_use.format(what=what, names=", ".join(imports)))
        for alias in node.names:
            name = alias.asname or alias.name
            self.new_name(name, Module())

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module
        imports = [
            f"{var(alias.name)}{self.pd._calling_it.format(alias=var(alias.asname)) if alias.asname else ""}"
            for alias in node.names
        ]
        what = str(
            self.pd.the_elements if len(imports) > 1
            else self.pd.the_element
        )
        self.append(node, self.pd.well_use_from_module.format(what=what, names=", ".join(imports), mod=var(module)))
        for alias in node.names:
            name = alias.asname or alias.name
            self.new_name(name, VarFuncClass())

    def visit_Expr(self, node: ast.Expr) -> None:
        # ast.Expr is an expr as a statement
        self.visit_stored(node.value)

    def visit_Assign(self, node: ast.Assign) -> None:
        # detect incrementation
        if len(node.targets) == 1:
            target = unparsed(node.targets[0])
            match node.targets[0]:
                case ast.Subscript(value, slice):
                    # TODO slice may not be a variable
                    target_desc = self.pd.position_i_of.format(
                        index=var(unparsed(slice)),
                        var=var(unparsed(value))
                    )
                case _:
                    target_desc = var(unparsed(node.targets[0]))

            match node.value:
                case ast.BinOp(ast.Name(src), ast.Add(), inc) | ast.BinOp(inc, ast.Add(), ast.Name(src)) if (
                    src == target
                ):
                    self.append(node, self.pd.add_)
                    self.visit(inc)
                    self.append(node, self.pd._to_var.format(var=target_desc))
                case ast.BinOp(ast.Name(src), ast.Sub(), dec) if src == target:
                    self.append(node, self.pd.remove_)
                    self.visit(dec)
                    self.append(node, self.pd._from_var.format(var=target_desc))
                case ast.BinOp(ast.Name(src), ast.Mult(), mul) | ast.BinOp(
                    mul, ast.Mult(), ast.Name(src)
                ) if (src == target):
                    self.append(node, self.pd.multiply_var_by_.format(var=target_desc))
                    self.visit(mul)
                case ast.BinOp(ast.Name(src), ast.Div() | ast.FloorDiv() as op, dec) if src == target:
                    self.append(node, self.pd.divide_var_by_.format(var=target_desc))
                    self.visit(dec)
                    if isinstance(op, ast.FloorDiv):
                        self.append(node, self.pd._as_integer_numbers)
                case _:
                    self.append(node, self.pd.in_var_store_.format(var=target_desc))
                    self.visit_stored(node.value)
        else:
            unhandled("multiple assignment")

        for varname in node.targets:
            self.new_name(varname, Var(type=None))

    def visit_stored(self, node: ast.expr) -> None:
        match node:
            case ast.Compare() | ast.BoolOp(ast.Or() | ast.And(), _):
                self.append(node, self.pd.true_false_according_do_)
                self.allow_break_for_next()
                self.visit(node)
            case _:
                self.visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            self.append(
                node,
                self.pd.prepare_var_for_type.format(
                    var=var(unparsed(node.target)),
                    type=self.readable_type(node.annotation)
                ),
            )
        else:
            self.append(
                node,
                self.pd.in_var_for_type_.format(
                    var=var(unparsed(node.target)),
                    type=self.readable_type(node.annotation)
                ),
            )
            self.append(node, self.pd._store_, allow_break=True)
            self.visit_stored(node.value)
        self.new_name(node.target, Var(type=node.annotation))

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        ident = unparsed(node.target)
        match node.op:
            case ast.Add():
                self.append(node, self.pd.add_)
                self.visit(node.value)
                self.append(node, self.pd._to_dest.format(dest=var(ident)))
            case ast.Sub():
                self.append(node, self.pd.subtract_src_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Mult():
                self.append(node, self.pd.multiply_by_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Div():
                self.append(node, self.pd.divide_by_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.FloorDiv():
                self.append(node, self.pd.int_divide_by_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Mod():
                self.append(node, self.pd.store_mod_.format(dest=var(ident), src=var(ident)))
                self.visit(node.value)
            case ast.Pow():
                self.append(node, self.pd.store_power_.format(dest=var(ident), src=var(ident)))
                self.visit(node.value)
            case _:
                self.append(node, self.pd.store_op_.format(dest=var(ident), src=var(ident), op=node.op))
                self.visit_stored(node.value)
        self.new_name(node.target, Var(type=None))

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        self.append(node, self.pd.the_expansion_of.format(expr=unparsed(node)[1:]))

    def new_name(self, node: ast.expr | str, t: NameInfo) -> None:
        match node:
            case ast.Name(id) | str(id):
                old = self._names.get(id)
                if old is not None and (isinstance(old, Var) and old.type is not None):
                    # we have better information from before, so we skip the update
                    pass
                else:
                    self._names[id] = t
            case _:
                pass

    # def name_is(self, name: str, t: _ClassInfo) -> bool:
    #     return self._names.get(name) == t

    def visit_Constant(self, node: ast.Constant) -> None:
        match node.value:
            case str(value):
                if len(value) == 0:
                    self.append(node, self.pd.empty_str)
                else:
                    self.append(node, f'"{value}"')
            case x if x == Ellipsis:
                self.append(node, self.pd.something_to_be_defined)
            case x if x == None:
                self.append(node, self.pd.empty_value)
            case _:
                self.append(node, f"{node.value}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        match node.op:
            case ast.USub():
                self.append(node, self.pd.the_opposite_of_)
                self.visit(node.operand)
            case ast.UAdd():
                # self.append(node, self.pd.the_same_as)
                self.visit(node.operand)
            case ast.Not():
                self.append(node, self.pd.the_logical_opposite_of_)
                self.visit(node.operand, insert_brace_if_complex=True)
            case _:
                unhandled(f"unary operator: {type(node.op).__name__}")

    def visit_BinOp(self, node: ast.BinOp) -> None:
        # detect modulo-zero checks
        match node:
            case ast.BinOp(left, ast.Mod(), ast.Constant(value)) if (
                n_digits := num_zeros_if_power_of_10(value)
            ) is not None:
                what = self.pd.the_units_digit_of_ if n_digits == 1 \
                    else self.pd.n_last_digits_of_.format(n=n_digits)
                self.visit(left)
                self.append(node, self.pd._modulo_.format(val=value, desc=what))
                self.visit(left)
                self.append(node, f")")

            case _:
                match node.op:
                    case ast.Add():
                        self.append(node, self.pd.the_sum_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._and_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Sub():
                        self.append(node, self.pd.the_difference_between_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._and_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Mult():
                        self.append(node, self.pd.the_product_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, f" × ")
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Div():
                        self.append(node, self.pd.the_quotient_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._divided_by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.FloorDiv():
                        self.append(node, self.pd.the_integer_quotient_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._divided_by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Mod():
                        self.append(node, self.pd.the_remainder_of_the_division_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Pow():
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, self.pd._to_the_power_of_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case _:
                        self.append(node, self.pd.the_result_of)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, f" {node.op} ")
                        self.visit(node.right, insert_brace_if_complex=True)

    def visit_Call(self, node: ast.Call) -> None:
        funcname = unparsed(node.func)
        args = node.args
        match funcname:
            case "print":
                if len(args) == 0:
                    self.append(node, self.pd.display_empty_line)
                else:
                    self.append(node, self.pd.display_)
                    for i, arg in enumerate(args):
                        if i > 0:
                            self.append(node, self.pd._and_)
                        self.visit(arg)

            case "math.sqrt":
                self.append(node, self.pd.the_square_root_of_)
                self.visit(args[0])
            case "math.ceil":
                self.visit(args[0])
                self.append(node, self.pd._rounded_up)
            case "math.floor":
                self.visit(args[0])
                self.append(node, self.pd._rounded_down)
            case "math.sin":
                self.append(node, self.pd.the_sine_of_)
                self.visit(args[0])
            case "math.cos":
                self.append(node, self.pd.the_cosine_of_)
                self.visit(args[0])
            case "math.tan":
                self.append(node, self.pd.the_tangent_of_)
                self.visit(args[0])
            case "round":
                self.append(node, self.pd.the_rounded_value_of)
                self.visit(args[0])
            case "input":
                if args:
                    self.append(node, self.pd.the_user_response_to_question_)
                    self.visit(args[0])
                else:
                    self.append(node, self.pd.what_the_user_will_type)
            case "str":
                self.append(node, self.pd.the_str_conversion_of_)
                self.visit(args[0])
            case "float":
                self.append(node, self.pd.the_float_conversion_of_)
                self.visit(args[0])
            case "int":
                self.append(node, self.pd.the_int_conversion_of_)
                self.visit(args[0])
            case "bool":
                self.append(node, self.pd.the_bool_conversion_of_)
                self.visit(args[0])
            case "abs":
                self.append(node, self.pd.the_absolute_value_of_)
                self.visit(args[0])
            case "type":
                self.append(node, self.pd.the_type_of_)
                self.visit(args[0])
            case "len":
                self.append(node, self.pd.the_length_of_)
                self.visit(args[0])
            case "list":
                if len(args) == 0:
                    self.append(node, self.pd.an_empty_list)
                else:
                    self.append(node, self.pd.the_list_conversion_of_)
                    self.visit(args[0])
            case "set":
                if len(args) == 0:
                    self.append(node, self.pd.an_empty_set)
                else:
                    self.append(node, self.pd.the_set_conversion_of_)
                    self.visit(args[0])
            case "tuple":
                if len(args) == 0:
                    self.append(node, self.pd.an_empty_tuple)
                else:
                    self.append(node, self.pd.the_tuple_conversion_of_)
                    self.visit(args[0])
            case "dict":
                if len(args) == 0:
                    self.append(node, self.pd.an_empty_dict)
                else:
                    self.append(node, self.pd.the_dict_conversion_of_)
                    self.visit(args[0])
            case "range":
                numargs = len(args)
                if numargs == 0:
                    self.append(node, self.pd.an_undefined_range)
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

                self.append(node, self.pd.the_range_from_)
                self.visit(from_, insert_brace_if_complex=True)
                self.append(node, self.pd._to_)
                self.visit(to, insert_brace_if_complex=True)
                if step is not None and not (isinstance(step, ast.Constant) and step.value == 1):
                    self.append(node, self.pd._with_a_step_of_)
                    self.visit(step, insert_brace_if_complex=True)

            case _:

                def append_args(first_prefix: str = "") -> None:
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

                            # string methods
                            case "startswith":
                                append_expr()
                                self.append(node, self.pd._starts_with_)
                                append_args()
                            case "endswith":
                                append_expr()
                                self.append(node, self.pd._ends_with_)
                                append_args()
                            case "upper":
                                self.append(node, self.pd.an_uppercase_copy_of_)
                                append_expr()
                            case "lower":
                                self.append(node, self.pd.a_lowercase_copy_of_)
                                append_expr()
                            case "capitalize":
                                self.append(node, self.pd.a_capitalized_copy_of_)
                                append_expr()
                            case "title":
                                self.append(node, self.pd.a_titled_copy_of_)
                                append_expr()
                            case "strip":
                                self.append(node, self.pd.a_trimmed_copy_of_)
                                append_expr()
                            case "lstrip":
                                self.append(node, self.pd.an_ltrimmed_copy_of_)
                                append_expr()
                            case "rstrip":
                                self.append(node, self.pd.an_rtrimmed_copy_of_)
                                append_expr()

                            # list methods
                            case "append":
                                self.append(node, self.pd.at_the_end_of_)
                                append_expr()
                                self.append(node, self.pd._append_)
                                append_args()
                            case "extend":
                                self.append(node, self.pd.at_the_end_of_)
                                append_expr()
                                is_literal = len(args) == 1 and (
                                    isinstance(args[0], ast.List) or isinstance(args[0], ast.Tuple)
                                )
                                if is_literal:
                                    self.append(node, self.pd._append_elements_)
                                    for arg in self.sep_join(args[0].elts):
                                        self.visit(arg)
                                else:
                                    self.append(node, self.pd._append_elements_of_)
                                    append_args()
                            case "insert":
                                if len(args) == 2:
                                    self.append(node, self.pd.at_position)
                                    self.visit(args[0])
                                    self.append(node, self.pd._in_)
                                    append_expr()
                                    self.append(node, self.pd._insert_)
                                    self.visit(args[1])
                                else:
                                    self.append(node, self.pd.in_)
                                    append_expr()
                                    self.append(node, self.pd._insert_undefined)
                            case "remove" | "discard":
                                # discard is different from remove, because it is only for sets and won't raise an error if the specified item does not exist, but remove will
                                self.append(node, self.pd.from_)
                                append_expr()
                                self.append(node, self.pd._remove_)
                                append_args()
                            case "pop":
                                self.append(node, self.pd.from_)
                                append_expr()
                                if len(args) == 0:
                                    self.append(node, self.pd._remove_last_item)
                                else:
                                    self.append(node, self.pd._remove_at_position_)
                                    self.visit(args[0])
                            case "clear":
                                self.append(node, self.pd.remove_all_elements_of_)
                                append_expr()
                            case "index":
                                numargs = len(args)
                                self.append(node, self.pd.index_in_)
                                append_expr()
                                if numargs == 0:
                                    self.append(node, self.pd._of_an_undefined_item)
                                else:
                                    self.append(node, self.pd._of_)
                                    self.visit(args[0])
                                    if numargs == 2:
                                        self.append(node, self.pd._starting_at_)
                                        self.visit(args[1])
                                        self.append(node, f")")
                                    elif numargs == 3:
                                        self.append(node, self.pd._between_position_)
                                        self.visit(args[1])
                                        self.append(node, self.pd._and_position_)
                                        self.visit(args[2])
                                        self.append(node, f")")

                            case "count":
                                self.append(node, self.pd.the_number_of_occurrences_in_)
                                append_expr()
                                self.append(node, self.pd._of_)
                                append_args()
                            case "sort":
                                self.append(node, self.pd.sort_)
                                append_expr()
                                # TODO key= and reverse= argument parsing
                            case "reverse":
                                self.append(node, self.pd.reverse_)
                                append_expr()
                            case "copy":
                                self.append(node, self.pd.a_copy_of_)
                                append_expr()

                            # additional set methods
                            case "add":
                                self.append(node, self.pd.in_)
                                append_expr()
                                self.append(node, self.pd._add_)
                                append_args()
                            # TODO there are others, like difference, intersection, isdisjoint, issubset, issuperset, symmetric_difference, union, etc.: https://www.w3schools.com/python/python_ref_set.asp

                            # generic methods
                            case _:
                                # TODO find if we are in an expression or a statement
                                is_statement = False
                                if is_statement:
                                    self.append(node, self.pd.call_method_.format(m=var(method)))
                                    append_expr()
                                    append_args(first_prefix=self.pd._with_)
                                else:
                                    self.append(node, self.pd.the_result_of_method_.format(m=var(method)))
                                    append_expr()
                                    append_args(first_prefix=self.pd._with_)
                    case _:
                        # TODO find if we are in an expression or a statement
                        is_statement = False
                        if is_statement:
                            self.append(node, self.pd.call_function.format(f=funcname))
                            append_args(first_prefix=self.pd._with_)
                        else:
                            self.append(node, self.pd.the_result_of_function.format(f=funcname))
                            append_args(first_prefix=self.pd._with_)

    def visit_Name(self, node: ast.Name) -> None:
        self.append(node, var(node.id))

    def visit_collection(self, node: ast.List | ast.Set | ast.Tuple, name: str) -> None:
        num_elems = len(node.elts)
        if num_elems == 0:
            self.append(node, self.pd.empty_collection.format(coll=name))
        elif num_elems == 1:
            self.append(node, self.pd.collection_with_one_item.format(coll=name))
            self.visit(node.elts[0])
        else:
            self.append(node, self.pd.collection_with_items_.format(coll=name))
            for elem in self.sep_join(node.elts):
                self.visit(elem, insert_brace_if_complex=True)

    def visit_List(self, node: ast.List) -> None:
        self.visit_collection(node, self.pd.a_list)

    def visit_Set(self, node: ast.Set) -> None:
        self.visit_collection(node, self.pd.a_set)

    def visit_Tuple(self, node: ast.Tuple) -> None:
        self.visit_collection(node, self.pd.a_tuple)

    def visit_Dict(self, node: ast.Dict) -> None:
        num_elems = len(node.keys)
        if num_elems == 0:
            self.append(node, self.pd.an_empty_dict)
        elif num_elems == 1:
            self.append(node, self.pd.a_dict_linking_)
            self.visit(node.keys[0])
            self.append(node, self.pd._to_)
            self.visit(node.values[0])
        else:
            self.append(node, self.pd.a_dict_linking_enum)
            for key, value in self.sep_join(zip(node.keys, node.values)):
                self.visit(key, allow_break=True)
                self.append(key, self.pd._to_)
                self.visit(value)

    def visit_Starred(self, node: ast.Starred) -> None:
        match node.value:
            case ast.Subscript():
                self.visit(node.value)
            case _:
                self.append(node, self.pd.the_elements_of_)
                self.visit(node.value)

    def visit_Pass(self, node: ast.Pass) -> None:
        self.append(node, self.pd.just_pass)

    def visit_Break(self, node: ast.Break) -> None:
        self.append(node, self.pd.break_loop)

    def visit_Continue(self, node: ast.Continue) -> None:
        self.append(node, self.pd.continue_loop)

    def visit_Return(self, node: ast.Return) -> None:
        if node.value is None:
            self.append(node, self.pd.function_return)
        else:
            self.append(node, self.pd.function_return_value_)
            self.visit(node.value)

    def visit_Yield(self, node: ast.Yield) -> None:
        if node.value is None:
            self.append(node, self.pd.yield_none)
        else:
            self.append(node, self.pd.yield_)
            self.visit(node.value)

    def visit_Try(self, node: ast.Try) -> None:
        self.append(node, self.pd.try_)
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.handlers:
            for handler in node.handlers:
                self.append(handler.body[0], self.pd.except_, linedelta=-1)
                # TODO: de type blabla
                self.indent()
                for stmt in handler.body:
                    self.visit(stmt)
                self.outdent()
        if node.finalbody:
            self.append(node.finalbody[0], self.pd.finally_, linedelta=-1)
            self.indent()
            for stmt in node.finalbody:
                self.visit(stmt)
            self.outdent()
        if node.orelse:
            self.append(node, self.pd.try_else_, linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_Await(self, node: ast.Await) -> None:
        self.append(node, self.pd.await_)
        self.visit(node.value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.append(node, self.pd.define_function_.format(name=var(node.name)))
        for arg in node.args.args:
            self.new_name(arg.arg, Var(type=arg.annotation))
        num_args = len(node.args.args)
        needs_and = num_args > 0

        def append_arg(arg: ast.arg) -> None:
            self.append(arg, var(arg.arg), allow_break=True)
            if arg.annotation:
                self.append(arg, " (")
                self.append(arg, self.readable_type(arg.annotation))
                self.append(arg, ")")

        if num_args == 0:
            self.append(node, self.pd.without_argument_)
        elif num_args == 1:
            self.append(node, self.pd.which_accepts_one_argument_)
            append_arg(arg)
            self.append(node, ", ")
        else:
            self.append(node, self.pd.which_accepts_n_arguments_.format(n=num_args))
            self.append(node, ", ")
            for arg in self.sep_join(node.args.args):
                append_arg(arg)
            self.append(node, ", ")
        if node.returns:
            if needs_and:
                self.append(node, self.pd.and_)
            match node.returns:
                case ast.Constant(None):
                    self.append(node, self.pd.which_returns_nothing, allow_break=True)
                case _:
                    self.append(
                        node,
                        self.pd.which_returns_this_.format(ret=self.readable_type(node.returns)),
                        allow_break=True
                    )
        self.append(node, self.pd.so_)

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.append(node, self.pd.an_anonymous_function_)
        for arg in node.args.args:
            self.new_name(arg.arg, Var(type=arg.annotation))
        num_args = len(node.args.args)
        if num_args == 0:
            self.append(node, self.pd.without_arguments)
        elif num_args == 1:
            self.append(node, self.pd.which_accepts_one_argument_)
            self.append(node, var(node.args.args[0].arg))
            self.append(node, ",")
            self.append(node, self.pd._and)
        else:
            self.append(node, self.pd.which_accepts_n_arguments_.format(n=num_args))
            for arg, is_last in track_last(node.args.args):
                if not is_last:
                    self.append(node, f", {var(arg.arg)}")
                else:
                    self.append(node, self.pd._and_ + var(arg.arg))
                    self.append(node, ",")
                    self.append(node, self.pd._and)
        self.append(node, self.pd._which_returns_, allow_break=True)
        self.visit(node.body)

    def visit_For(self, node: ast.For) -> None:
        # loop variable
        loop_var = unparsed(node.target)
        is_throwaway_var = loop_var == "_"
        match node.iter:

            # range(len(...))
            case ast.Call(ast.Name("range"), [ast.Call(ast.Name("len"), [iterable])]):
                self.append(node, self.pd.repeat_as_many_times_as_elements_in_)
                self.visit(iterable, insert_brace_if_complex=True)
                if not is_throwaway_var:
                    self.append(node, self.pd._counting_with_var_from_0.format(var=var(loop_var)), allow_break=True)
                else:
                    self.append(node, f":")

            # numerical range
            case ast.Call(
                ast.Name(id="range"),
                args=[to] | [ast.Constant(value=0), to] | [ast.Constant(value=0), to, ast.Constant(value=1)],
            ):
                with_loop_var = (
                    "" if is_throwaway_var else self.pd._counting_with_var_from_0.format(var=var(loop_var))
                )

                self.append(node, self.pd.repeat_)
                self.visit(to, insert_brace_if_complex=True)
                self.append(node, self.pd._times_details.format(details=with_loop_var))

            case ast.Call(ast.Name("enumerate"), [iterable, *other_args]):
                self.append(node, self.pd.repeat_for_each_item_of_)
                self.visit(iterable)
                if is_throwaway_var:
                    self.append(node, f":")
                else:
                    match node.target:
                        case ast.Tuple([ast.Name(index), ast.Name(elem)]):
                            self.append(
                                node,
                                self.pd._which_well_call_and_number_from_.format(elem=var(elem), index=var(index)),
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
                with_loop_var = "" if is_throwaway_var else self.pd._which_well_call.format(elem=var(loop_var))
                self.append(node, self.pd.repeat_for_each_character_in_.format(str=value, details=with_loop_var))
                self.append(node, ":")

            case _:
                self.append(node, self.pd.repeat_for_each_item_of_)
                self.visit(node.iter)
                with_loop_var = "" if is_throwaway_var else self.pd._which_well_call.format(elem=var(loop_var))
                self.append(node, f"{with_loop_var}:")

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.orelse:
            self.append(node.orelse[0], self.pd.if_loop_wasnt_broken_, linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_While(self, node: ast.While) -> None:
        match node.test:
            case ast.Constant(True | 1):
                self.append(node, self.pd.repeat_indefinitely_)
            case _:
                self.append(node, self.pd.while_)
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
                        self.append(node, self.pd.a_copy_of_)
                        self.visit(node.value)
                    else:
                        # upper is given
                        self.append(node, self.pd.the_plural_)
                        self.visit(upper, insert_brace_if_complex=True)
                        self.append(node, self.pd._first_elements_of_)
                        self.visit(node.value)
                else:
                    # lower is given
                    if upper_is_none_or_end:
                        self.append(node, self.pd.the_elements_of_)
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, self.pd._starting_at_position_)
                        self.visit(lower, insert_brace_if_complex=True)
                    else:
                        # upper is given
                        self.append(node, self.pd.the_elements_of_)
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, self.pd._from_position_)
                        self.visit(lower, insert_brace_if_complex=True)
                        self.append(node, self.pd._to_position_)
                        self.visit(upper, insert_brace_if_complex=True)

                if not step_none_or_one:
                    self.append(node, self.pd._with_one_elements_out_of.format(step=step))

            case ast.Name(id) if len(id) == 1:
                self.append(node, self.pd.ith_element_of_.format(index=var(id)))
                self.visit(node.value)
            case index:
                self.append(node, self.pd.the_element_at_position_)
                self.visit(index)
                self.append(node, self.pd._of_)
                self.visit(node.value)

    def visit_If(self, node: ast.If) -> None:
        self.append(node, self.pd.if_)
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
                self.append(node.orelse[0], self.pd.else_comma_)
                self.visit(node.orelse[0])
            else:
                self.append(node.orelse[0], self.pd.else_colon_, linedelta=-1)
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
                self.append(node, self.pd._is_false)
            case ast.Name():
                self.visit(node, insert_brace_if_complex=True)
                self.append(node, self.pd._is_true)
            case _:
                self.visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        first_level_condition = isinstance(self._stack[-2], (ast.If, ast.While))
        suffix = "" if not first_level_condition else self.pd._and_if
        op_str = (
            self.pd.and_op if isinstance(node.op, ast.And)
            else self.pd.or_op if isinstance(node.op, ast.Or)
            else "???"
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
                        self.append(node, self.pd._is_even)
                    case (False, 2):
                        self.append(node, self.pd._is_odd)
                    case (True, _):
                        self.append(node, self.pd._is_multiple_of.format(n=value))
                    case (False, _):
                        self.append(node, self.pd._is_not_multiple_of.format(n=value))

            # Boolean checks
            case ast.Compare(ast.Constant(True), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_true)
            case ast.Compare(ast.Constant(False), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_false)
            case ast.Compare(ast.Constant(True), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_not_true)
            case ast.Compare(ast.Constant(False), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_not_false)

            # None checks
            case ast.Compare(ast.Constant(None), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_empty)

            case ast.Compare(ast.Constant(None), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, self.pd._is_not_empty)

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
                self.append(node, f" {self.compop(op)} ")
                self.visit(right)

            # standard double-op < or > comparisons
            case ast.Compare(
                lower,
                [ast.Lt() | ast.LtE(), ast.Lt() | ast.LtE()] | [ast.Gt() | ast.GtE(), ast.Gt() | ast.GtE()],
                [ast.Name(name), upper],
            ):

                def is_inclusive_op(op: ast.cmpop) -> bool:
                    return isinstance(op, (ast.LtE, ast.GtE))

                self.append(node, var(name))
                self.append(node, self.pd._is_between_)
                self.visit(lower)
                self.append(
                    node,
                    self.pd._inclusive if is_inclusive_op(node.ops[0])
                    else self.pd._exclusive
                )
                self.append(node, self.pd._and_)
                self.visit(upper)
                self.append(
                    node,
                    self.pd._inclusive if is_inclusive_op(node.ops[1])
                    else self.pd._exclusive
                )

            case _:

                def compop_to_str(op: ast.cmpop) -> str:
                    match op:
                        case ast.Eq():
                            return "=="
                        case ast.NotEq():
                            return "!="
                        case ast.Lt():
                            return "<"
                        case ast.LtE():
                            return "<="
                        case ast.Gt():
                            return ">"
                        case ast.GtE():
                            return ">="
                        case _:
                            return "???"

                self.visit(node.left)
                for op, comp in zip(node.ops, node.comparators):
                    self.append(node, f" {compop_to_str(op)} ")
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


def annotate_code(
    source: str,
    pseudocode_format: PseudocodeFormat,
    pseudocode_dictionary: PseudocodeDictionary,
    dump_ast: bool = False
) -> AnnotationResult | None:

    MAX_LINE_WIDTH = 60
    V_BAR = "│"
    PYTHON_ANN_SEP = "#" + V_BAR
    CONTINUATION_MARK = "└╴"
    PREAMBLE_LENGTH = 4
    MIN_CODE_WIDTH = 25
    LEFT_COL_HEADER = pseudocode_dictionary.Code
    RIGHT_COL_HEADER = pseudocode_dictionary.Interpretation

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

    analyzer = Analyzer(pseudocode_format, pseudocode_dictionary)
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

    use_markdown = pseudocode_format == markdown_pseudocode_format
    format_code_line = (
        (lambda src: "`" + src + "`" if src else "&nbsp;" if use_markdown else "")
        if use_markdown
        else lambda src: src
    )

    sep = PYTHON_ANN_SEP if pseudocode_format == python_pseudocode_format else "|"
    header_sep = "" if pseudocode_format != python_pseudocode_format \
        else f"{'"""':{max_src_width}}{margin_left}{sep}"

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
        pseu = pseudocode_dictionary.post_process_pseudocode(pseu)
        code_line = format_code_line(src)
        if i == last_index and len(code_line.strip()) + len(pseu.strip()) == 0:
            # keep last line without annotation if empty, reduces glitches in editor
            output_lines.append(code_line)
        else:
            output_lines.append(f"{code_line:{max_src_width}}{margin_left}{sep}{margin_right}{pseu}")

    return AnnotationResult(
        input_had_preamble,
        input_continuations,
        output_lines,
        output_continuations
    )


def annotate_code_and_get_as_json(code: str, lang: str) -> str | None:
    result_json: str | None = None

    pseudocode_format = python_pseudocode_format

    pseudocode_dictionary: PseudocodeDictionary = language_pseudocode_dictionaries[lang]

    if isinstance(code, str):
        result = annotate_code(code, pseudocode_format, pseudocode_dictionary)
        if result:
            result_json = json.dumps(result._asdict())
        else:
            # syntax error
            pass

    return result_json
