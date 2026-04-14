
# Imports

from .pseudocode_dictionary import PseudocodeDictionary

# Class Definition

class EnglishPseudocodeDictionary(PseudocodeDictionary):

    # Headers
    Code = "Code"
    Interpretation = "Interpretation"

    # Types
    an_int = "an integer number"
    ints = "integer numbers"
    a_float = "a decimal number"
    floats = "decimal numbers"
    a_str = "a string"
    strs = "strings"
    a_bool = "a true/false value"
    bools = "true/false values"
    a_list = "a list"
    lists = "lists"
    a_set = "a set"
    sets = "sets"
    a_dict = "a dict"
    dicts = "dicts"
    a_tuple = "a tuple"
    tuples = "tuples"

    # Assignment
    prepare_var_for_type = "prepare {var} to store {type}"
    in_var_store_ = "in {var}, store "
    in_var_for_type_ = "in {var}, intended for {type},"
    _store_ = " store "
    add_ = "add "
    _to_var = " to {var}"
    remove_ = "subtract "
    _from_var = " from {var}"
    multiply_var_by_ = "multiply {var} by "
    divide_var_by_ = "divide {var} by "
    _as_integer_numbers = " as integer numbers"
    position_i_of = "position {index} of {var}"

    # Collection types
    list_or_set_of = "{cont} of {elem}"
    dict_of = "{cont} linking {key} to {value}"
    dict_malformed = "{cont} with badly defined items"
    tuple_of = "{cont} with {elem}"
    container_of = "{cont} of {elem}"

    _and_ = " and "
    and_ = "and "
    _and = " and"

    # CompOp
    is_equal_to = "is equal to"
    is_different_from = "is different from"
    is_smaller_than = "is smaller than"
    is_smaller_than_or_equal_to = "is smaller than or equal to"
    is_greater_than = "is greater than"
    is_greater_than_or_equal_to = "is greater than or equal to"
    is_ = "is"
    is_not = "is not"
    is_in = "is in"
    is_not_in = "is not in"
    _is_between_ = " is between "
    _inclusive = " (inclusive)"
    _exclusive = " (exclusive)"

    # Imports
    well_use = "we'll use {what} {names}"
    well_use_from_module = "we'll use {what} {names} from module {mod}"
    the_module = "the module"
    the_modules = "the modules"
    the_element = "the element"
    the_elements = "the elements"
    _calling_it = " (calling it {alias})"

    add_ = "add "
    _to_dest = " to {dest}"
    subtract_src_ = "diminish {dest} by "
    multiply_by_ = "multiply {dest} by "
    divide_by_ = "divide {dest} by "
    int_divide_by_ = "integer divide {dest} by "
    store_mod_ = "in {dest}, store the remainder of the division of {src} by "
    store_power_ = "in {dest}, store {src} to the power of "
    store_op_ = "in {dest}, store the result of {src} {op} "

    the_expansion_of = "the expansion of {expr}"

    # Constants
    empty_str = "an empty string"
    something_to_be_defined = "something to be defined"
    empty_value = "an empty value"

    # UnOp
    the_opposite_of_ = "the opposite of "
    the_same_as_ = "the same as "
    the_logical_opposite_of_ = "the logical opposite of "

    # BinOp
    the_units_digit_of_ = "the units digit of "
    n_last_digits_of_ = "the {n} last digits of "
    _modulo_ = " modulo {val} (so {desc}"
    the_sum_of_ = "the sum of "
    the_difference_between_ = "the difference between "
    the_product_ = "the product "
    the_quotient_of_ = "the quotient of "
    _divided_by_ = " divided by "
    the_integer_quotient_of_ = "the integer quotient of "
    the_remainder_of_the_division_of_ = "the remainder of the division of "
    _by_ = " by "
    _to_the_power_of_ = " to the power of "
    the_result_of = "the result of "

    # Call
    display_empty_line = "display an empty line"
    display_ = "display "
    the_square_root_of_ = "the square root of "
    the_rounded_value_of = "the rounded value of "
    _rounded_up = " rounded up"
    _rounded_down = " rounded down"
    the_sine_of_ = "the sine of "
    the_cosine_of_ = "the cosine of "
    the_tangent_of_ = "the tangent of "
    the_user_response_to_question_ = "the user response to the question "
    what_the_user_will_type = "what the user will type"
    the_str_conversion_of_ = "the conversion to a character string of "
    the_float_conversion_of_ = "the conversion to a decimal number of "
    the_int_conversion_of_ = "the conversion to an integer number of "
    the_bool_conversion_of_ = "the conversion to a true/false value of "
    the_absolute_value_of_ = "the absolute value of "
    the_type_of_ = "the type of "
    the_length_of_ = "the length of "
    an_empty_list = "an empty list"
    the_list_conversion_of_ = "the conversion to a list of "
    an_empty_set = "an empty set"
    the_set_conversion_of_ = "the conversion to a set of "
    an_empty_tuple = "an empty tuple"
    the_tuple_conversion_of_ = "the conversion to a tuple of "
    an_empty_dict = "an empty dictionary"
    the_dict_conversion_of_ = "the conversion to a dictionary of "
    an_undefined_range = "an undefined range"
    the_range_from_ = "the range from "
    _to_ = " to "
    _with_a_step_of_ = " with a step of "

    _starts_with_ = " starts with "
    _ends_with_ = " ends with "
    an_uppercase_copy_of_ = "an uppercase copy of "
    a_lowercase_copy_of_ = "a lowercase copy of "
    a_capitalized_copy_of_ = "a copy with the first letter capitalized of "
    a_titled_copy_of_ = "a copy with each word capitalized of "
    a_trimmed_copy_of_ = "a copy with whitespace removed from the beginning and end of "
    an_ltrimmed_copy_of_ = "a copy with whitespace removed from the beginning of "
    an_rtrimmed_copy_of_ = "a copy with whitespace removed from the end of "
    at_the_end_of_ = "at the end of "
    _append_ = ", append "
    _append_elements_ = ", append elements "
    _append_elements_of_ = ", append all elements of "
    at_position = "at position "
    _in_ = " in "
    _insert_ = ", insert "
    in_ = "in "
    _insert_undefined = ", insert something badly defined"
    from_ = "from "
    _remove_ = ", remove "
    _remove_last_item = ", remove the last item"
    _remove_at_position_ = ", remove the item at position "
    remove_all_elements_of_ = "remove all elements of "
    index_in_ = "the position in "
    _of_an_undefined_item = " of an undefined item"
    _of_ = " of "
    _starting_at_ = " (starting at position "
    _between_position_ = " (between position "
    _and_position_ = " and position "
    the_number_of_occurrences_in_ = "the number of occurrences in "
    sort_ = "sort "
    reverse_ = "reverse the order of the items of "
    a_copy_of_ = "a copy of "
    _add_ = ", add "

    call_function = "call the function {f}"
    the_result_of_function = "the result of the function {f}"
    call_method_ = "call the method {m} of "
    the_result_of_method_ = "the result of the method {m} of "
    _with_ = " with "

    # Collections
    empty_collection = "empty {coll}"
    collection_with_one_item = "{coll} with one item"
    collection_with_items_ = "{coll} with items "
    a_list = "a list"
    a_set = "a set"
    a_tuple = "a tuple"
    an_empty_dict = "an empty dictionary"
    a_dict_linking_ = "a dictionary linking "
    a_dict_linking_enum = "a dictionary linking: "

    # Misc
    the_elements_of_ = "the elements of "
    just_pass = "don’t do anything"

    # Control flow
    break_loop = "get out of the loop"
    continue_loop = "continue to the next iteration"
    function_return = "get out of the function"
    function_return_value_ = "get out of the function returning "
    yield_none = "generate an empty value"
    yield_ = "generate "
    try_ = "try to do this:"
    except_ = "in case of an error:"
    finally_ = "in any case, finish doing this:"
    try_else_ = "if there were no error:"
    await_ = "wait for "
    if_ = "if "
    else_comma_ = "else, "
    else_colon_ = "else:"

    # For
    repeat_as_many_times_as_elements_in_ = "repeat as many times as there are elements in "
    _counting_with_var_from_0 = " (counting with {var} from 0):"
    repeat_ = "repeat "
    _times_details = " times{details}"
    repeat_for_each_item_of_ = "repeat for each item of "
    _which_well_call_and_number_from_ = " (which we’ll call {elem} and number {index} from "
    _which_well_call = " (which we’ll call {elem})"
    repeat_for_each_character_in_ = 'repeat for each character in "{str}"{details}'
    if_loop_wasnt_broken_ = "if the loop wasn’t broken:"
    repeat_indefinitely_ = "repeat indefinitely:"
    while_ = "while "

    # Def/lambdas
    define_function_ = "define the function {name}, "
    without_argument_ = "without any arguments, "
    which_accepts_one_argument_ = "which accepts one argument, "
    which_accepts_n_arguments_ = "which accepts {n} arguments"
    which_returns_nothing = "which returns nothing, "
    _which_returns_ = " which returns "
    which_returns_this_ = "which returns {ret}, "
    so_ = "like so:"
    an_anonymous_function_ = "an anonymous function "
    without_arguments = "without any arguments"

    # Subscripts
    a_copy_of_ = "a copy of "
    the_plural_ = "the "
    _first_elements_of_ = " first elements of "
    the_elements_of_ = "the elements of "
    _starting_at_position_ = " starting at position "
    _from_position_ = " from position "
    _to_position_ = " to "
    _with_one_elements_out_of = " with one element out of {step}"
    ith_element_of_ = "the {index}th element of "
    the_element_at_position_ = "element "

    # Conditions
    _is_true = " is true"
    _is_not_true = " is not true"
    _is_false = " is false"
    _is_not_false = " is not false"
    _and_if = " if"
    and_op = "and"
    or_op = "or"
    _is_even = " is an even number"
    _is_odd = " is an odd number"
    _is_multiple_of = " is a multiple of {n}"
    _is_not_multiple_of = " is not a multiple of {n}"
    _is_empty = " is empty"
    _is_not_empty = " is not empty"
    true_false_according_do_ = "true/false according to if "

    def get_language_code(self) -> str:
        return 'en'

    def post_process_pseudocode(self, pseudocode: str) -> str:
        return (
            pseudocode
                .replace(" a i", " an i") # e.g. "an int"
                .replace(" a e", " an e") # e.g. "an empty list"
        )
