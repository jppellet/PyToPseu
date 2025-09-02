import ast
import json
from dataclasses import dataclass
from enum import Enum
from pprint import pformat, pprint
from types import EllipsisType, NoneType
from typing import Any, Callable, Iterable, NamedTuple, Type, TypeVar

from typing_extensions import TypeIs

KNOWN_LANGS = {"en", "fr"}

current_lang = "en"


def set_lang(lang: str) -> None:
    global current_lang
    if lang in KNOWN_LANGS:
        current_lang = lang
    else:
        print(f"Warning: unknown language '{lang}', defaulting to English")
        current_lang = "en"


@dataclass
class s:
    en: str
    fr: str

    @property
    def str(self) -> str:
        return self.fr if current_lang == "fr" else self.en

    def __str__(self) -> str:
        return self.str

    def __add__(self, other: Any) -> str:
        return self.str + str(other)

    def __radd__(self, other: Any) -> str:
        return str(other) + self.str


@dataclass
class sf:
    en: str
    fr: str

    def format(self, **kwargs: str) -> str:
        return (self.fr if current_lang == "fr" else self.en).format(**kwargs)


class S:

    # Headers
    Code = s("Code", "Code")
    Interpretation = s("Interpretation", "Interprétation")

    # Types
    an_int: s = s("an integer number", "un nombre entier")
    ints = s("integer numbers", "nombres entiers")
    a_float = s("a decimal number", "un nombre à virgule")
    floats = s("decimal numbers", "nombres à virgule")
    a_str = s("a string", "une chaîne de caractères")
    strs = s("strings", "chaînes de caractères")
    a_bool = s("a true/false value", "une valeur vrai/faux")
    bools = s("true/false values", "valeurs vrai/faux")
    a_list = s("a list", "une liste")
    lists = s("lists", "listes")
    a_set = s("a set", "un ensemble")
    sets = s("sets", "ensembles")
    a_dict = s("a dict", "un dictionnaire")
    dicts = s("dicts", "dictionnaires")
    a_tuple = s("a tuple", "un tuple")
    tuples = s("tuples", "tuples")

    # Assignment
    prepare_var_for_type = sf("prepare {var} to store {type}", "on prépare {var} pour y stocker {type}")
    in_var_store_ = sf("in {var}, store ", "dans {var}, stocke ")
    in_var_for_type_ = sf("in {var}, intended for {type},", "dans {var}, prévu pour {type},")
    _store_ = s(" store ", " stocke ")
    add_ = s("add ", "ajoute ")
    _to_var = sf(" to {var}", " à {var}")
    remove_ = s("subtract ", "soustrais ")
    _from_var = sf(" from {var}", " de {var}")
    multiply_var_by_ = sf("multiply {var} by ", "multiplie {var} par ")
    divide_var_by_ = sf("divide {var} by ", "divise {var} par ")
    _as_integer_numbers = s(" as integer numbers", " en nombres entiers")
    position_i_of = sf("position {index} of {var}", "à la position {index} de {var}")

    # Collection types
    list_or_set_of = sf("{cont} of {elem}", "{cont} de {elem}")
    dict_of = sf("{cont} linking {key} to {value}", "{cont} reliant des {key} à des {value}")
    dict_malformed = sf("{cont} with badly defined items", "{cont} d’éléments mal définis")
    tuple_of = sf("{cont} with {elem}", "{cont} avec {elem}")
    container_of = sf("{cont} of {elem}", "{cont} de {elem}")

    _and_ = s(" and ", " et ")
    and_ = s("and ", "et ")
    _and = s(" and", " et")

    # CompOp
    is_equal_to = s("is equal to", "est égal à")
    is_different_from = s("is different from", "est différent de")
    is_smaller_than = s("is smaller than", "est plus petit que")
    is_smaller_than_or_equal_to = s("is smaller than or equal to", "est plus petit que ou égal à")
    is_greater_than = s("is greater than", "est plus grand que")
    is_greater_than_or_equal_to = s("is greater than or equal to", "est plus grand que ou égal à")
    is_ = s("is", "est")
    is_not = s("is not", "n'est pas")
    is_in = s("is in", "fait partie de")
    is_not_in = s("is not in", "ne fait pas partie de")
    _is_between_ = s(" is between ", " est entre ")
    _inclusive = s(" (inclusive)", " (inclusif)")
    _exclusive = s(" (exclusive)", " (exclusif)")

    # Imports
    well_use = sf("we'll use {what} {names}", "on va utiliser {what} {names}")
    well_use_from_module = sf(
        "we'll use {what} {names} from module {mod}", "on va utiliser {what} {names} du module {mod}"
    )
    the_module = s("the module", "le module")
    the_modules = s("the modules", "les modules")
    the_element = s("the element", "l’élément")
    the_elements = s("the elements", "les éléments")
    _calling_it = sf(" (calling it {alias})", " (en l’appelant {alias})")

    add_ = s("add ", "ajoute ")
    _to_dest = sf(" to {dest}", " à {dest}")
    subtract_src_ = sf("diminish {dest} by ", "diminue {dest} de ")
    multiply_by_ = sf("multiply {dest} by ", "multiplie {dest} par ")
    divide_by_ = sf("divide {dest} by ", "divise {dest} par ")
    int_divide_by_ = sf("integer divide {dest} by ", "divise en nombres entiers {dest} par ")
    store_mod_ = sf(
        "in {dest}, store the remainder of the division of {src} by ",
        "dans {dest}, stocke le reste de la division de {src} par ",
    )
    store_power_ = sf(
        "in {dest}, store {src} to the power of ", "dans {dest}, stocke {src} à la puissance de "
    )
    store_op_ = sf(
        "in {dest}, store the result of {src} {op} ", "dans {dest}, stocke le résultat de {src} {op} "
    )

    the_expansion_of = sf("the expansion of {expr}", "l’expansion de {expr}")

    # Constants
    empty_str = s("an empty string", "une chaîne de caractères vide")
    something_to_be_defined = s("something to be defined", "quelque chose à définir")
    empty_value = s("an empty value", "une valeur vide")

    # UnOp
    the_opposite_of_ = s("the opposite of ", "l’opposé de ")
    the_same_as_ = s("the same as ", "le même que ")
    the_logical_opposite_of_ = s("the logical opposite of ", "le contraire de ")

    # BinOp
    the_units_digit_of_ = s("the units digit of ", "le chiffre des unités de ")
    n_last_digits_of_ = sf("the {n} last digits of ", "les {n} derniers chiffres de ")
    _modulo_ = sf(" modulo {val} (so {desc}", " modulo {val} (donc {desc}")
    the_sum_of_ = s("the sum of ", "la somme de ")
    the_difference_between_ = s("the difference between ", "la différence entre ")
    the_product_ = s("the product ", "le produit ")
    the_quotient_of_ = s("the quotient of ", "le quotient de ")
    _divided_by_ = s(" divided by ", " divisé par ")
    the_integer_quotient_of_ = s("the integer quotient of ", "le quotient entier de ")
    the_remainder_of_the_division_of_ = s("the remainder of the division of ", "le reste de la division de ")
    _by_ = s(" by ", " par ")
    _to_the_power_of_ = s(" to the power of ", " à la puissance ")
    the_result_of = s("the result of ", "le résultat de ")

    # Call
    display_empty_line = s("display an empty line", "affiche une ligne vide")
    display_ = s("display ", "affiche ")
    the_square_root_of_ = s("the square root of ", "la racine carrée de ")
    the_rounded_value_of = s("the rounded value of ", "la valeur arrondie de ")
    _rounded_up = s(" rounded up", " arrondi vers le haut")
    _rounded_down = s(" rounded down", " arrondi vers le bas")
    the_sine_of_ = s("the sine of ", "le sinus de ")
    the_cosine_of_ = s("the cosine of ", "le cosinus de ")
    the_tangent_of_ = s("the tangent of ", "la tangente de ")
    the_user_response_to_question_ = s(
        "the user response to the question ", "la réponse de l’utilisateur à la question "
    )
    what_the_user_will_type = s("what the user will type", "ce que l’utilisateur va taper")
    the_str_conversion_of_ = s(
        "the conversion to a character string of ", "la conversion en chaîne de caractères de "
    )
    the_float_conversion_of_ = s(
        "the conversion to a decimal number of ", "la conversion en nombre à virgule de "
    )
    the_int_conversion_of_ = s(
        "the conversion to an integer number of ", "la conversion en nombre entier de "
    )
    the_bool_conversion_of_ = s("the conversion to a true/false value of ", "la conversion en vrai/faux de ")
    the_absolute_value_of_ = s("the absolute value of ", "la valeur absolue de ")
    the_type_of_ = s("the type of ", "le type de ")
    the_length_of_ = s("the length of ", "la longueur de ")
    an_empty_list = s("an empty list", "une liste vide")
    the_list_conversion_of_ = s("the conversion to a list of ", "la conversion en liste de ")
    an_empty_set = s("an empty set", "un ensemble vide")
    the_set_conversion_of_ = s("the conversion to a set of ", "la conversion en ensemble de ")
    an_empty_tuple = s("an empty tuple", "un tuple vide")
    the_tuple_conversion_of_ = s("the conversion to a tuple of ", "la conversion en tuple de ")
    an_empty_dict = s("an empty dictionary", "un dictionnaire vide")
    the_dict_conversion_of_ = s("the conversion to a dictionary of ", "la conversion en dictionnaire de ")
    an_undefined_range = s("an undefined range", "une plage non définie")
    the_range_from_ = s("the range from ", "la plage de ")
    _to_ = s(" to ", " à ")
    _with_a_step_of_ = s(" with a step of ", " avec un pas de ")

    _starts_with_ = s(" starts with ", " commence par ")
    _ends_with_ = s(" ends with ", " finit par ")
    an_uppercase_copy_of_ = s("an uppercase copy of ", "une copie tout en majuscules de ")
    a_lowercase_copy_of_ = s("a lowercase copy of ", "une copie tout en minuscules de ")
    a_capitalized_copy_of_ = s(
        "a copy with the first letter capitalized of ", "une copie avec la première lettre en majuscule de "
    )
    a_titled_copy_of_ = s(
        "a copy with each word capitalized of ",
        "une copie avec la première lettre de chaque mot en majuscule de ",
    )
    a_trimmed_copy_of_ = s(
        "a copy with whitespace removed from the beginning and end of ",
        "une copie sans espaces de début et de fin de ",
    )
    an_ltrimmed_copy_of_ = s(
        "a copy with whitespace removed from the beginning of ", "une copie sans espaces de début de "
    )
    an_rtrimmed_copy_of_ = s(
        "a copy with whitespace removed from the end of ", "une copie sans espaces de fin de "
    )
    at_the_end_of_ = s("at the end of ", "à la fin de ")
    _append_ = s(", append ", ", ajoute ")
    _append_elements_ = s(", append elements ", ", ajoute les éléments ")
    _append_elements_of_ = s(", append all elements of ", ", ajoute tous les éléments de ")
    at_position = s("at position ", "à la position ")
    _in_ = s(" in ", " de ")
    _insert_ = s(", insert ", ", insère ")
    in_ = s("in ", "dans ")
    _insert_undefined = s(", insert something badly defined", ", insère quelque chose de mal défini")
    from_ = s("from ", "de ")
    _remove_ = s(", remove ", ", retire ")
    _remove_last_item = s(", remove the last item", ", supprime le dernier élément")
    _remove_at_position_ = s(", remove the item at position ", ", supprime l’élément à la position ")
    remove_all_elements_of_ = s("remove all elements of ", "supprime tous les éléments de ")
    index_in_ = s("the position in ", "la position dans ")
    _of_an_undefined_item = s(" of an undefined item", " d’un élément mal défini")
    _of_ = s(" of ", " de ")
    _starting_at_ = s(" (starting at position ", " (à partir de la position ")
    _between_position_ = s(" (between position ", " (entre la position ")
    _and_position_ = s(" and position ", " et la position ")
    the_number_of_occurrences_in_ = s("the number of occurrences in ", "le nombre d’occurrences dans ")
    sort_ = s("sort ", "trie ")
    reverse_ = s("reverse the order of the items of ", "inverse l’ordre des éléments de ")
    a_copy_of_ = s("a copy of ", "une copie de ")
    _add_ = s(", add ", ", inclus ")

    call_function = sf("call the function {f}", "appelle la fonction {f}")
    the_result_of_function = sf("the result of the function {f}", "le résultat de la fonction {f}")
    call_method_ = sf("call the method {m} of ", "appelle la méthode {m} de ")
    the_result_of_method_ = sf("the result of the method {m} of ", "le résultat de la méthode {m} de ")
    _with_ = s(" with ", " avec ")

    # Collections
    empty_collection = sf("empty {coll}", "{coll} vide")
    collection_with_one_item = sf("{coll} with one item", "{coll} avec un seul élément")
    collection_with_items_ = sf("{coll} with items ", "{coll} avec les éléments ")
    a_list = s("a list", "une liste")
    a_set = s("a set", "un ensemble")
    a_tuple = s("a tuple", "un tuple")
    an_empty_dict = s("an empty dictionary", "un dictionnaire vide")
    a_dict_linking_ = s("a dictionary linking ", "un dictionnaire reliant ")
    a_dict_linking_enum = s("a dictionary linking: ", "un dictionnaire reliant: ")

    # Misc
    the_elements_of_ = s("the elements of ", "les éléments de ")
    just_pass = s("don’t do anything", "ne fais rien de spécial")

    # Control flow
    break_loop = s("get out of the loop", "sors de la boucle")
    continue_loop = s("continue to the next iteration", "passe à l’itération suivante")
    function_return = s("get out of the function", "sors de la fonction")
    function_return_value_ = s("get out of the function returning ", "sors de la fonction en renvoyant ")
    yield_none = s("generate an empty value", "génère une valeur vide")
    yield_ = s("generate ", "génère ")
    try_ = s("try to do this:", "essaie de faire ceci:")
    except_ = s("in case of an error:", "en cas d’erreur:")
    finally_ = s("in any case, finish doing this:", "dans tous les cas, finis par ceci:")
    try_else_ = s("if there were no error:", "s’il n'y a pas eu d’erreur:")
    await_ = s("wait for ", "attends ")
    if_ = s("if ", "si ")
    else_comma_ = s("else, ", "sinon, ")
    else_colon_ = s("else:", "sinon:")

    # For
    repeat_as_many_times_as_elements_in_ = s(
        "repeat as many times as there are elements in ", "répète autant de fois qu’il y a d’éléments dans "
    )
    _counting_with_var_from_0 = sf(
        " (counting with {var} from 0):", " (en comptant avec {var} à partir de 0):"
    )
    repeat_ = s("repeat ", "répète ")
    _times_details = sf(" times{details}", " fois{details}")
    repeat_for_each_item_of_ = s("repeat for each item of ", "répète pour chaque élément de ")
    _which_well_call_and_number_from_ = sf(
        " (which we’ll call {elem} and number {index} from ",
        " (qu'on va appeler {elem} et numéroter {index} depuis ",
    )
    _which_well_call = sf(" (which we’ll call {elem})", " (qu'on va appeler {elem})")
    repeat_for_each_character_in_ = sf(
        'repeat for each character in "{str}"{details}', 'répète pour chaque caractère dans "{str}"{details}'
    )
    if_loop_wasnt_broken_ = s("if the loop wasn’t broken:", "si la boucle n’a pas été interrompue:")
    repeat_indefinitely_ = s("repeat indefinitely:", "répète indéfiniment:")
    while_ = s("while ", "tant que ")

    # Def/lambdas
    define_function_ = sf("define the function {name}, ", "définis la fonction {name}, ")
    without_argument_ = s("without any arguments, ", "sans argument, ")
    which_accepts_one_argument_ = s("which accepts one argument, ", "qui demande un argument, ")
    which_accepts_n_arguments_ = sf("which accepts {n} arguments", "qui demande {n} arguments")
    which_returns_nothing = s("which returns nothing, ", "qui ne renvoie rien, ")
    _which_returns_ = s(" which returns ", "qui renvoie ")
    which_returns_this_ = sf("which returns {ret}, ", "qui renvoie {ret}, ")
    so_ = s("like so:", "ainsi:")
    an_anonymous_function_ = s("an anonymous function ", "une fonction anonyme ")
    without_arguments = s("without any arguments", "sans argument")

    # Subscripts
    a_copy_of_ = s("a copy of ", "une copie de ")
    the_plural_ = s("the ", "les ")
    _first_elements_of_ = s(" first elements of ", " premiers éléments de ")
    the_elements_of_ = s("the elements of ", "les éléments de ")
    _starting_at_position_ = s(" starting at position ", " à partir de la position ")
    _from_position_ = s(" from position ", " de la position ")
    _to_position_ = s(" to ", " à ")
    _with_one_elements_out_of = sf(" with one element out of {step}", " avec un élément sur {step}")
    ith_element_of_ = sf("the {index}th element of ", "le {index}ᵉ élément de ")
    the_element_at_position_ = s("element ", "l’élément ")

    # Conditions
    _is_true = s(" is true", " est vrai")
    _is_not_true = s(" is not true", " n’est pas vrai")
    _is_false = s(" is false", " est faux")
    _is_not_false = s(" is not false", " n’est pas faux")
    _and_if = s(" if", " que")
    and_op = s("and", "et")
    or_op = s("or", "ou")
    _is_even = s(" is an even number", " est un nombre pair")
    _is_odd = s(" is an odd number", " est un nombre impair")
    _is_multiple_of = sf(" is a multiple of {n}", " est un multiple de {n}")
    _is_not_multiple_of = sf(" is not a multiple of {n}", " n’est pas un multiple de {n}")
    _is_empty = s(" is empty", " est vide")
    _is_not_empty = s(" is not empty", " n’est pas vide")
    true_false_according_do_ = s("true/false according to if ", "vrai/faux selon si ")


class Format(Enum):
    TEXT = "txt"
    MARKDOWN = "md"
    PYTHON = "py"


# See https://docs.python.org/3/library/ast.html#module-ast

CURRENT_LINE = -1
ASTERISKS = ["*", "†", "‡", "§", "‖", "¶", "Δ", "◊"]

T = TypeVar("T")


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


def track_last(iterable: Iterable[T]) -> Iterable[tuple[T, bool]]:
    it = iter(iterable)
    prev = next(it)
    for current in it:
        yield prev, False
        prev = current
    yield prev, True


def unparsed(expr: ast.AST) -> str:
    return ast.unparse(expr)


def readable_type(expr: ast.expr, plural: bool = False) -> str:

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
                        return S.an_int if not plural else S.ints, int
                    case "float":
                        return S.a_float if not plural else S.floats, float
                    case "str":
                        return S.a_str if not plural else S.strs, str
                    case "bool":
                        return S.a_bool if not plural else S.bools, bool
                    case "list" | "List":
                        return S.a_list if not plural else S.lists, list
                    case "set" | "Set":
                        return S.a_set if not plural else S.sets, set
                    case "dict" | "Dict" | "defaultdict":
                        return S.a_dict if not plural else S.dicts, dict
                    case "tuple" | "Tuple":
                        return S.a_tuple if not plural else S.tuples, tuple
                    case _:
                        return simpletype, None

            # parametrized types
            case ast.Subscript(paramtype, typeparams):
                basedesc, basetype = helper(paramtype, plural)
                if basetype is list or basetype is set:
                    elem = readable_type(typeparams, plural=True)
                    return S.list_or_set_of.format(cont=basedesc, elem=elem), basetype
                if basetype is dict:
                    match typeparams:
                        case ast.Tuple([keytype, valuetype]):
                            return (
                                S.dict_of.format(
                                    cont=basedesc,
                                    key=readable_type(keytype, plural=True),
                                    value=readable_type(valuetype, plural=True),
                                ),
                                basetype,
                            )
                        case _:
                            return S.dict_malformed.format(cont=basedesc), basetype
                if basetype is tuple:
                    return (
                        S.tuple_of.format(cont=basedesc, elem=readable_type(typeparams, plural=True)),
                        basetype,
                    )

                return (
                    S.container_of.format(cont=basedesc, elem=readable_type(typeparams, plural=True)),
                    basetype,
                )

            # multiple type parameters
            case ast.Tuple(elts):
                return ", ".join(readable_type(e, plural) for e in elts), None  # not tuple

        # all the rest
        unparsed = ast.unparse(expr)
        unhandled(f"type with AST of class {type(expr).__name__}, {unparsed}")
        return unparsed, None

    return str(helper(expr, plural)[0])


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
    def helper():
        match op:
            case ast.Eq():
                return S.is_equal_to
            case ast.NotEq():
                return S.is_different_from
            case ast.Lt():
                return S.is_smaller_than
            case ast.LtE():
                return S.is_smaller_than_or_equal_to
            case ast.Gt():
                return S.is_greater_than
            case ast.GtE():
                return S.is_greater_than_or_equal_to
            case ast.Is():
                return S.is_
            case ast.IsNot():
                return S.is_not
            case ast.In():
                return S.is_in
            case ast.NotIn():
                return S.is_not_in
            case _:
                unhandled(f"comparison operator: {type(op).__name__}")
                return ast.unparse(op)

    return str(helper())


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
    def __init__(self, format: Format) -> None:
        self.format = format
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
        msg: str | s,
        linedelta: int = 0,
        allow_break: bool = False,
    ) -> None:
        line = CURRENT_LINE if node is None else node.lineno
        allow_break = allow_break or self._allow_break_for_next
        self._allow_break_for_next = False
        self._out_buffer.append(OutStr(line + linedelta, self._indent, str(msg), allow_break))

    A = TypeVar("A", bound=ast.expr | ast.stmt | ast.arg)

    def sep_join(self, items: Iterable[A], sep: str = ", ", last_sep: str | None = None) -> Iterable[A]:
        """
        Join items with separators, like "a, b et c"
        """
        if last_sep is None:
            last_sep = S._and_.str
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
        what = str(S.the_modules if len(imports) > 1 else S.the_module)
        self.append(node, S.well_use.format(what=what, names=", ".join(imports)))
        for alias in node.names:
            name = alias.asname or alias.name
            self.new_name(name, Module())

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module
        imports = [
            f"{var(alias.name)}{S._calling_it.format(alias=var(alias.asname)) if alias.asname else ""}"
            for alias in node.names
        ]
        what = str(S.the_elements if len(imports) > 1 else S.the_element)
        self.append(node, S.well_use_from_module.format(what=what, names=", ".join(imports), mod=var(module)))
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
                    target_desc = S.position_i_of.format(index=var(unparsed(slice)), var=var(unparsed(value)))
                case _:
                    target_desc = var(unparsed(node.targets[0]))

            match node.value:
                case ast.BinOp(ast.Name(src), ast.Add(), inc) | ast.BinOp(inc, ast.Add(), ast.Name(src)) if (
                    src == target
                ):
                    self.append(node, S.add_)
                    self.visit(inc)
                    self.append(node, S._to_var.format(var=target_desc))
                case ast.BinOp(ast.Name(src), ast.Sub(), dec) if src == target:
                    self.append(node, S.remove_)
                    self.visit(dec)
                    self.append(node, S._from_var.format(var=target_desc))
                case ast.BinOp(ast.Name(src), ast.Mult(), mul) | ast.BinOp(
                    mul, ast.Mult(), ast.Name(src)
                ) if (src == target):
                    self.append(node, S.multiply_var_by_.format(var=target_desc))
                    self.visit(mul)
                case ast.BinOp(ast.Name(src), ast.Div() | ast.FloorDiv() as op, dec) if src == target:
                    self.append(node, S.divide_var_by_.format(var=target_desc))
                    self.visit(dec)
                    if isinstance(op, ast.FloorDiv):
                        self.append(node, S._as_integer_numbers)
                case _:
                    self.append(node, S.in_var_store_.format(var=target_desc))
                    self.visit_stored(node.value)
        else:
            unhandled("multiple assignment")

        for varname in node.targets:
            self.new_name(varname, Var(type=None))

    def visit_stored(self, node: ast.expr) -> None:
        match node:
            case ast.Compare() | ast.BoolOp(ast.Or() | ast.And(), _):
                self.append(node, S.true_false_according_do_)
                self.allow_break_for_next()
                self.visit(node)
            case _:
                self.visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            self.append(
                node,
                S.prepare_var_for_type.format(
                    var=var(unparsed(node.target)), type=readable_type(node.annotation)
                ),
            )
        else:
            self.append(
                node,
                S.in_var_for_type_.format(
                    var=var(unparsed(node.target)), type=readable_type(node.annotation)
                ),
            )
            self.append(node, S._store_, allow_break=True)
            self.visit_stored(node.value)
        self.new_name(node.target, Var(type=node.annotation))

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        ident = unparsed(node.target)
        match node.op:
            case ast.Add():
                self.append(node, S.add_)
                self.visit(node.value)
                self.append(node, S._to_dest.format(dest=var(ident)))
            case ast.Sub():
                self.append(node, S.subtract_src_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Mult():
                self.append(node, S.multiply_by_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Div():
                self.append(node, S.divide_by_.format(dest=var(ident)))
                self.visit(node.value)
            case ast.FloorDiv():
                self.append(node, S.int_divide_by.format(dest=var(ident)))
                self.visit(node.value)
            case ast.Mod():
                self.append(node, S.store_mod.format(dest=var(ident), src=var(ident)))
                self.visit(node.value)
            case ast.Pow():
                self.append(node, S.store_power_.format(dest=var(ident), src=var(ident)))
                self.visit(node.value)
            case _:
                self.append(node, S.store_op_.format(dest=var(ident), src=var(ident), op=node.op))
                self.visit_stored(node.value)
        self.new_name(node.target, Var(type=None))

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        self.append(node, S.the_expansion_of.format(expr=unparsed(node)[1:]))

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
                    self.append(node, S.empty_str)
                else:
                    self.append(node, f'"{value}"')
            case x if x == Ellipsis:
                self.append(node, S.something_to_be_defined)
            case x if x == None:
                self.append(node, S.empty_value)
            case _:
                self.append(node, f"{node.value}")

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        match node.op:
            case ast.USub():
                self.append(node, S.the_opposite_of_)
                self.visit(node.operand)
            case ast.UAdd():
                # self.append(node, S.the_same_as)
                self.visit(node.operand)
            case ast.Not():
                self.append(node, S.the_logical_opposite_of)
                self.visit(node.operand, insert_brace_if_complex=True)
            case _:
                unhandled(f"unary operator: {type(node.op).__name__}")

    def visit_BinOp(self, node: ast.BinOp) -> None:
        # detect modulo-zero checks
        match node:
            case ast.BinOp(left, ast.Mod(), ast.Constant(value)) if (
                n_digits := num_zeros_if_power_of_10(value)
            ) is not None:
                what = S.the_units_digit_of_.str if n_digits == 1 else S.n_last_digits_of_.format(n=n_digits)
                self.visit(left)
                self.append(node, S._modulo_.format(val=value, desc=what))
                self.visit(left)
                self.append(node, f")")

            case _:
                match node.op:
                    case ast.Add():
                        self.append(node, S.the_sum_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._and_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Sub():
                        self.append(node, S.the_difference_between_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._and_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Mult():
                        self.append(node, S.the_product_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, f" × ")
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Div():
                        self.append(node, S.the_quotient_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._divided_by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.FloorDiv():
                        self.append(node, S.the_integer_quotient_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._divided_by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Mod():
                        self.append(node, S.the_remainder_of_the_division_of_)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._by_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case ast.Pow():
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, S._to_the_power_of_)
                        self.visit(node.right, insert_brace_if_complex=True)
                    case _:
                        self.append(node, S.the_result_of)
                        self.visit(node.left, insert_brace_if_complex=True)
                        self.append(node, f" {node.op} ")
                        self.visit(node.right, insert_brace_if_complex=True)

    def visit_Call(self, node: ast.Call) -> None:
        funcname = unparsed(node.func)
        args = node.args
        match funcname:
            case "print":
                if len(args) == 0:
                    self.append(node, S.display_empty_line)
                else:
                    self.append(node, S.display_)
                    for i, arg in enumerate(args):
                        if i > 0:
                            self.append(node, S._and_)
                        self.visit(arg)

            case "math.sqrt":
                self.append(node, S.the_square_root_of_)
                self.visit(args[0])
            case "math.ceil":
                self.visit(args[0])
                self.append(node, S._rounded_up)
            case "math.floor":
                self.visit(args[0])
                self.append(node, S._rounded_down)
            case "math.sin":
                self.append(node, S.the_sine_of_)
                self.visit(args[0])
            case "math.cos":
                self.append(node, S.the_cosine_of_)
                self.visit(args[0])
            case "math.tan":
                self.append(node, S.the_tangent_of_)
                self.visit(args[0])
            case "round":
                self.append(node, S.the_rounded_value_of)
                self.visit(args[0])
            case "input":
                if args:
                    self.append(node, S.the_user_response_to_question_)
                    self.visit(args[0])
                else:
                    self.append(node, S.what_the_user_will_type)
            case "str":
                self.append(node, S.the_str_conversion_of_)
                self.visit(args[0])
            case "float":
                self.append(node, S.the_float_conversion_of_)
                self.visit(args[0])
            case "int":
                self.append(node, S.the_int_conversion_of_)
                self.visit(args[0])
            case "bool":
                self.append(node, S.the_bool_conversion_of_)
                self.visit(args[0])
            case "abs":
                self.append(node, S.the_absolute_value_of_)
                self.visit(args[0])
            case "type":
                self.append(node, S.the_type_of_)
                self.visit(args[0])
            case "len":
                self.append(node, S.the_length_of_)
                self.visit(args[0])
            case "list":
                if len(args) == 0:
                    self.append(node, S.an_empty_list)
                else:
                    self.append(node, S.the_list_conversion_of_)
                    self.visit(args[0])
            case "set":
                if len(args) == 0:
                    self.append(node, S.an_empty_set)
                else:
                    self.append(node, S.the_set_conversion_of_)
                    self.visit(args[0])
            case "tuple":
                if len(args) == 0:
                    self.append(node, S.an_empty_tuple)
                else:
                    self.append(node, S.the_tuple_conversion_of_)
                    self.visit(args[0])
            case "dict":
                if len(args) == 0:
                    self.append(node, S.an_empty_dict)
                else:
                    self.append(node, S.the_dict_conversion_of_)
                    self.visit(args[0])
            case "range":
                numargs = len(args)
                if numargs == 0:
                    self.append(node, S.an_undefined_range)
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

                self.append(node, S.the_range_from_)
                self.visit(from_, insert_brace_if_complex=True)
                self.append(node, S._to_)
                self.visit(to, insert_brace_if_complex=True)
                if step is not None and not (isinstance(step, ast.Constant) and step.value == 1):
                    self.append(node, S._with_a_step_of_)
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
                                self.append(node, S._starts_with_)
                                append_args()
                            case "endswith":
                                append_expr()
                                self.append(node, S._ends_with_)
                                append_args()
                            case "upper":
                                self.append(node, S.an_uppercase_copy_of_)
                                append_expr()
                            case "lower":
                                self.append(node, S.a_lowercase_copy_of_)
                                append_expr()
                            case "capitalize":
                                self.append(node, s.a_capitalized_copy_of_)
                                append_expr()
                            case "title":
                                self.append(node, S.a_titled_copy_of_)
                                append_expr()
                            case "strip":
                                self.append(node, S.a_trimmed_copy_of_)
                                append_expr()
                            case "lstrip":
                                self.append(node, S.an_ltrimmed_copy_of_)
                                append_expr()
                            case "rstrip":
                                self.append(node, S.an_rtrimmed_copy_of_)
                                append_expr()

                            # list methods
                            case "append":
                                self.append(node, S.at_the_end_of_)
                                append_expr()
                                self.append(node, S._append_)
                                append_args()
                            case "extend":
                                self.append(node, S.at_the_end_of_)
                                append_expr()
                                is_literal = len(args) == 1 and (
                                    isinstance(args[0], ast.List) or isinstance(args[0], ast.Tuple)
                                )
                                if is_literal:
                                    self.append(node, S._append_elements_)
                                    for arg in self.sep_join(args[0].elts):
                                        self.visit(arg)
                                else:
                                    self.append(node, S._append_elements_of_)
                                    append_args()
                            case "insert":
                                if len(args) == 2:
                                    self.append(node, S.at_position)
                                    self.visit(args[0])
                                    self.append(node, S._in_)
                                    append_expr()
                                    self.append(node, S._insert_)
                                    self.visit(args[1])
                                else:
                                    self.append(node, S.in_)
                                    append_expr()
                                    self.append(node, S._insert_undefined)
                            case "remove" | "discard":
                                # discard is different from remove, because it is only for sets and won't raise an error if the specified item does not exist, but remove will
                                self.append(node, S.from_)
                                append_expr()
                                self.append(node, S._remove_)
                                append_args()
                            case "pop":
                                self.append(node, S.from_)
                                append_expr()
                                if len(args) == 0:
                                    self.append(node, S._remove_last_item)
                                else:
                                    self.append(node, S._remove_at_position_)
                                    self.visit(args[0])
                            case "clear":
                                self.append(node, S.remove_all_elements_of_)
                                append_expr()
                            case "index":
                                numargs = len(args)
                                self.append(node, S.index_in_)
                                append_expr()
                                if numargs == 0:
                                    self.append(node, S._of_an_undefined_item)
                                else:
                                    self.append(node, S._of_)
                                    self.visit(args[0])
                                    if numargs == 2:
                                        self.append(node, S._starting_at_)
                                        self.visit(args[1])
                                        self.append(node, f")")
                                    elif numargs == 3:
                                        self.append(node, S._between_position_)
                                        self.visit(args[1])
                                        self.append(node, S._and_position_)
                                        self.visit(args[2])
                                        self.append(node, f")")

                            case "count":
                                self.append(node, S.the_number_of_occurrences_in_)
                                append_expr()
                                self.append(node, S._of_)
                                append_args()
                            case "sort":
                                self.append(node, S.sort_)
                                append_expr()
                                # TODO key= and reverse= argument parsing
                            case "reverse":
                                self.append(node, S.reverse_)
                                append_expr()
                            case "copy":
                                self.append(node, S.a_copy_of_)
                                append_expr()

                            # additional set methods
                            case "add":
                                self.append(node, S.in_)
                                append_expr()
                                self.append(node, S._add_)
                                append_args()
                            # TODO there are others, like difference, intersection, isdisjoint, issubset, issuperset, symmetric_difference, union, etc.: https://www.w3schools.com/python/python_ref_set.asp

                            # generic methods
                            case _:
                                # TODO find if we are in an expression or a statement
                                is_statement = False
                                if is_statement:
                                    self.append(node, S.call_method_.format(m=var(method)))
                                    append_expr()
                                    append_args(first_prefix=S._with_.str)
                                else:
                                    self.append(node, S.the_result_of_method_.format(m=var(method)))
                                    append_expr()
                                    append_args(first_prefix=S._with_.str)
                    case _:
                        # TODO find if we are in an expression or a statement
                        is_statement = False
                        if is_statement:
                            self.append(node, S.call_function.format(f=funcname))
                            append_args(first_prefix=S._with_.str)
                        else:
                            self.append(node, S.the_result_of_function.format(f=funcname))
                            append_args(first_prefix=S._with_.str)

    def visit_Name(self, node: ast.Name) -> None:
        self.append(node, var(node.id))

    def visit_collection(self, node: ast.List | ast.Set | ast.Tuple, name: str) -> None:
        num_elems = len(node.elts)
        if num_elems == 0:
            self.append(node, S.empty_collection.format(coll=name))
        elif num_elems == 1:
            self.append(node, S.collection_with_one_item.format(coll=name))
            self.visit(node.elts[0])
        else:
            self.append(node, S.collection_with_items_.format(coll=name))
            for elem in self.sep_join(node.elts):
                self.visit(elem, insert_brace_if_complex=True)

    def visit_List(self, node: ast.List) -> None:
        self.visit_collection(node, S.a_list)

    def visit_Set(self, node: ast.Set) -> None:
        self.visit_collection(node, S.a_set)

    def visit_Tuple(self, node: ast.Tuple) -> None:
        self.visit_collection(node, S.a_tuple)

    def visit_Dict(self, node: ast.Dict) -> None:
        num_elems = len(node.keys)
        if num_elems == 0:
            self.append(node, S.an_empty_dict)
        elif num_elems == 1:
            self.append(node, S.a_dict_linking_)
            self.visit(node.keys[0])
            self.append(node, S._to_)
            self.visit(node.values[0])
        else:
            self.append(node, S.a_dict_linking_enum)
            for key, value in self.sep_join(zip(node.keys, node.values)):
                self.visit(key, allow_break=True)
                self.append(key, S._to_)
                self.visit(value)

    def visit_Starred(self, node: ast.Starred) -> None:
        match node.value:
            case ast.Subscript():
                self.visit(node.value)
            case _:
                self.append(node, S.the_elements_of_)
                self.visit(node.value)

    def visit_Pass(self, node: ast.Pass) -> None:
        self.append(node, S.just_pass)

    def visit_Break(self, node: ast.Break) -> None:
        self.append(node, S.break_loop)

    def visit_Continue(self, node: ast.Continue) -> None:
        self.append(node, S.continue_loop)

    def visit_Return(self, node: ast.Return) -> None:
        if node.value is None:
            self.append(node, S.function_return)
        else:
            self.append(node, S.function_return_value_)
            self.visit(node.value)

    def visit_Yield(self, node: ast.Yield) -> None:
        if node.value is None:
            self.append(node, S.yield_none)
        else:
            self.append(node, S.yield_)
            self.visit(node.value)

    def visit_Try(self, node: ast.Try) -> None:
        self.append(node, S.try_)
        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.handlers:
            for handler in node.handlers:
                self.append(handler.body[0], S.except_, linedelta=-1)
                # TODO: de type blabla
                self.indent()
                for stmt in handler.body:
                    self.visit(stmt)
                self.outdent()
        if node.finalbody:
            self.append(node.finalbody[0], S.finally_, linedelta=-1)
            self.indent()
            for stmt in node.finalbody:
                self.visit(stmt)
            self.outdent()
        if node.orelse:
            self.append(node, S.try_else_, linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_Await(self, node: ast.Await) -> None:
        self.append(node, S.await_)
        self.visit(node.value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.append(node, S.define_function_.format(name=var(node.name)))
        for arg in node.args.args:
            self.new_name(arg.arg, Var(type=arg.annotation))
        num_args = len(node.args.args)
        needs_and = num_args > 0

        def append_arg(arg: ast.arg) -> None:
            self.append(arg, var(arg.arg), allow_break=True)
            if arg.annotation:
                self.append(arg, " (")
                self.append(arg, readable_type(arg.annotation))
                self.append(arg, ")")

        if num_args == 0:
            self.append(node, S.without_argument_)
        elif num_args == 1:
            self.append(node, S.which_accepts_one_argument_)
            append_arg(arg)
            self.append(node, ", ")
        else:
            self.append(node, S.which_accepts_n_arguments_.format(n=num_args))
            self.append(node, ", ")
            for arg in self.sep_join(node.args.args):
                append_arg(arg)
            self.append(node, ", ")
        if node.returns:
            if needs_and:
                self.append(node, S.and_)
            match node.returns:
                case ast.Constant(None):
                    self.append(node, S.which_returns_nothing, allow_break=True)
                case _:
                    self.append(
                        node, S.which_returns_this_.format(ret=readable_type(node.returns)), allow_break=True
                    )
        self.append(node, S.so_)

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.append(node, S.an_anonymous_function_)
        for arg in node.args.args:
            self.new_name(arg.arg, Var(type=arg.annotation))
        num_args = len(node.args.args)
        if num_args == 0:
            self.append(node, S.without_arguments)
        elif num_args == 1:
            self.append(node, S.which_accepts_one_argument_)
            self.append(node, var(node.args.args[0].arg))
            self.append(node, ",")
            self.append(node, S._and)
        else:
            self.append(node, S.which_accepts_n_arguments_.format(n=num_args))
            for arg, is_last in track_last(node.args.args):
                if not is_last:
                    self.append(node, f", {var(arg.arg)}")
                else:
                    self.append(node, S._and_ + var(arg.arg))
                    self.append(node, ",")
                    self.append(node, S._and)
        self.append(node, S._which_returns_, allow_break=True)
        self.visit(node.body)

    def visit_For(self, node: ast.For) -> None:
        # loop variable
        loop_var = unparsed(node.target)
        is_throwaway_var = loop_var == "_"
        match node.iter:

            # range(len(...))
            case ast.Call(ast.Name("range"), [ast.Call(ast.Name("len"), [iterable])]):
                self.append(node, S.repeat_as_many_times_as_elements_in_)
                self.visit(iterable, insert_brace_if_complex=True)
                if not is_throwaway_var:
                    self.append(node, S._counting_with_var_from_0.format(var=var(loop_var)), allow_break=True)
                else:
                    self.append(node, f":")

            # numerical range
            case ast.Call(
                ast.Name(id="range"),
                args=[to] | [ast.Constant(value=0), to] | [ast.Constant(value=0), to, ast.Constant(value=1)],
            ):
                with_loop_var = (
                    "" if is_throwaway_var else S._counting_with_var_from_0.format(var=var(loop_var))
                )

                self.append(node, S.repeat_)
                self.visit(to, insert_brace_if_complex=True)
                self.append(node, S._times_details.format(details=with_loop_var))

            case ast.Call(ast.Name("enumerate"), [iterable, *other_args]):
                self.append(node, S.repeat_for_each_item_of_)
                self.visit(iterable)
                if is_throwaway_var:
                    self.append(node, f":")
                else:
                    match node.target:
                        case ast.Tuple([ast.Name(index), ast.Name(elem)]):
                            self.append(
                                node,
                                S._which_well_call_and_number_from_.format(elem=var(elem), index=var(index)),
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
                with_loop_var = "" if is_throwaway_var else S._which_well_call.format(elem=var(loop_var))
                self.append(node, S.repeat_for_each_character_in_.format(str=value, details=with_loop_var))
                self.append(node, ":")

            case _:
                self.append(node, S.repeat_for_each_item_of_)
                self.visit(node.iter)
                with_loop_var = "" if is_throwaway_var else S._which_well_call.format(elem=var(loop_var))
                self.append(node, f"{with_loop_var}:")

        self.indent()
        for stmt in node.body:
            self.visit(stmt)
        self.outdent()
        if node.orelse:
            self.append(node.orelse[0], S.if_loop_wasnt_broken_, linedelta=-1)
            self.indent()
            for stmt in node.orelse:
                self.visit(stmt)
            self.outdent()

    def visit_While(self, node: ast.While) -> None:
        match node.test:
            case ast.Constant(True | 1):
                self.append(node, S.repeat_indefinitely_)
            case _:
                self.append(node, S.while_)
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
                        self.append(node, S.a_copy_of_)
                        self.visit(node.value)
                    else:
                        # upper is given
                        self.append(node, S.the_plural_)
                        self.visit(upper, insert_brace_if_complex=True)
                        self.append(node, S._first_elements_of_)
                        self.visit(node.value)
                else:
                    # lower is given
                    if upper_is_none_or_end:
                        self.append(node, S.the_elements_of_)
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, S._starting_at_position_)
                        self.visit(lower, insert_brace_if_complex=True)
                    else:
                        # upper is given
                        self.append(node, S.the_elements_of_)
                        self.visit(node.value, insert_brace_if_complex=True)
                        self.append(node, S._from_position_)
                        self.visit(lower, insert_brace_if_complex=True)
                        self.append(node, S._to_position_)
                        self.visit(upper, insert_brace_if_complex=True)

                if not step_none_or_one:
                    self.append(node, S._with_one_elements_out_of.format(step=step))

            case ast.Name(id) if len(id) == 1:
                self.append(node, S.ith_element_of_.format(index=var(id)))
                self.visit(node.value)
            case index:
                self.append(node, S.the_element_at_position_)
                self.visit(index)
                self.append(node, S._of_)
                self.visit(node.value)

    def visit_If(self, node: ast.If) -> None:
        self.append(node, S.if_)
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
                self.append(node.orelse[0], S.else_comma_)
                self.visit(node.orelse[0])
            else:
                self.append(node.orelse[0], S.else_colon_, linedelta=-1)
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
                self.append(node, S._is_false)
            case ast.Name():
                self.visit(node, insert_brace_if_complex=True)
                self.append(node, S._is_true)
            case _:
                self.visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        first_level_condition = isinstance(self._stack[-2], (ast.If, ast.While))
        suffix = "" if not first_level_condition else S._and_if
        op_str = (
            S.and_op if isinstance(node.op, ast.And) else S.or_op if isinstance(node.op, ast.Or) else "???"
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
                        self.append(node, S._is_even)
                    case (False, 2):
                        self.append(node, S._is_odd)
                    case (True, _):
                        self.append(node, S._is_multiple_of.format(n=value))
                    case (False, _):
                        self.append(node, S._is_not_multiple_of.format(n=value))

            # Boolean checks
            case ast.Compare(ast.Constant(True), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, S._is_true)
            case ast.Compare(ast.Constant(False), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, S._is_false)
            case ast.Compare(ast.Constant(True), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(True)]
            ):
                self.visit(expr)
                self.append(node, S._is_not_true)
            case ast.Compare(ast.Constant(False), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(False)]
            ):
                self.visit(expr)
                self.append(node, S._is_not_false)

            # None checks
            case ast.Compare(ast.Constant(None), [ast.Eq() | ast.Is()], [expr]) | ast.Compare(
                expr, [ast.Eq() | ast.Is()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, S._is_empty)

            case ast.Compare(ast.Constant(None), [ast.NotEq() | ast.IsNot()], [expr]) | ast.Compare(
                expr, [ast.NotEq() | ast.IsNot()], [ast.Constant(None)]
            ):
                self.visit(expr)
                self.append(node, S._is_not_empty)

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

            # standard double-op < or > comparisons
            case ast.Compare(
                lower,
                [ast.Lt() | ast.LtE(), ast.Lt() | ast.LtE()] | [ast.Gt() | ast.GtE(), ast.Gt() | ast.GtE()],
                [ast.Name(name), upper],
            ):

                def is_inclusive_op(op: ast.cmpop) -> bool:
                    return isinstance(op, (ast.LtE, ast.GtE))

                self.append(node, var(name))
                self.append(node, S._is_between_)
                self.visit(lower)
                self.append(node, S._inclusive if is_inclusive_op(node.ops[0]) else S._exclusive)
                self.append(node, S._and_)
                self.visit(upper)
                self.append(node, S._inclusive if is_inclusive_op(node.ops[1]) else S._exclusive)

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


def frenchify(s: str) -> str:
    return (
        s.replace(" à le ", " au ")
        .replace(" à les ", " aux ")
        .replace(" de les ", " des ")
        .replace(" de le ", " du ")
        .replace(" de e", " d’e")
    )


def englishify(s: str) -> str:
    return (
        s.replace(" a i", " an i")  # e.g., an int
        .replace(" a e", " an e") # an empty list
    )


def annotate_file(file: str, format: Format, lang: str, dump_ast: bool = False) -> None:
    set_lang(lang)
    print(f"Processing '{file}' in lang={lang}")

    with open(file, "r", encoding="utf8") as source_file:
        source = source_file.read()

    annotated = annotate_code(source, format, dump_ast)
    if not annotated:
        print("Syntax error")
        return

    ext = {Format.TEXT: ".txt", Format.MARKDOWN: ".md", Format.PYTHON: "_ann.py"}[format]
    outfile = os.path.splitext(file)[0] + "_" + current_lang + ext

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
    LEFT_COL_HEADER = S.Code.str
    RIGHT_COL_HEADER = S.Interpretation.str

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
        if current_lang == "fr":
            pseu = frenchify(pseu)
        elif current_lang == "en":
            pseu = englishify(pseu)
        code_line = format_code_line(src)
        if i == last_index and len(code_line.strip()) + len(pseu.strip()) == 0:
            # keep last line without annotation if empty, reduces glitches in editor
            output_lines.append(code_line)
        else:
            output_lines.append(f"{code_line:{max_src_width}}{margin_left}{sep}{margin_right}{pseu}")

    return AnnotationResult(input_had_preamble, input_continuations, output_lines, output_continuations)


def annotate_all(format: Format) -> None:
    for file in sorted(os.listdir("sample_src")):
        if file.endswith(".py") and not file.endswith("_ann.py"):
            for lang in KNOWN_LANGS:
                annotate_file(os.path.join("sample_src", file), format, lang)


result_json: str | None = None
if __name__ == "__main__":
    # check if local var __user_code__ exists
    format = Format.PYTHON

    local_vars = locals()

    if "__user_lang__" in local_vars:
        set_lang(local_vars["__user_lang__"])

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
        import sys

        file = sys.argv[1] if len(sys.argv) > 1 else None

        if file:
            for lang in KNOWN_LANGS:
                annotate_file(file, format, lang)
        else:
            annotate_all(format)

result_json
