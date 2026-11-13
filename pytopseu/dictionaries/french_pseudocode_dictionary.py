
# Imports

from .pseudocode_dictionary import PseudocodeDictionary

# Class Definition

class FrenchPseudocodeDictionary(PseudocodeDictionary):

    # Headers
    Code = "Code"
    Interpretation = "Interprétation"

    # Types
    an_int = "un nombre entier"
    ints = "nombres entiers"
    a_float = "un nombre à virgule"
    floats = "nombres à virgule"
    a_str = "une chaîne de caractères"
    strs = "chaînes de caractères"
    a_bool = "une valeur vrai/faux"
    bools = "valeurs vrai/faux"
    a_list = "une liste"
    lists = "listes"
    a_set = "un ensemble"
    sets = "ensembles"
    a_dict = "un dictionnaire"
    dicts = "dictionnaires"
    a_tuple = "un tuple"
    tuples = "tuples"

    # Assignment
    prepare_var_for_type = "on prépare {var} pour y stocker {type}"
    in_var_store_ = "dans {var}, stocke "
    in_var_for_type_ = "dans {var}, prévu pour {type},"
    _store_ = " stocke "
    add_ = "ajoute "
    _to_var = " à {var}"
    remove_ = "soustrais "
    _from_var = " de {var}"
    multiply_var_by_ = "multiplie {var} par "
    divide_var_by_ = "divise {var} par "
    _as_integer_numbers = " en nombres entiers"
    position_i_of = "à la position {index} de {var}"

    # Collection types
    list_or_set_of = "{cont} de {elem}"
    dict_of = "{cont} reliant des {key} à des {value}"
    dict_malformed = "{cont} d’éléments mal définis"
    tuple_of = "{cont} avec {elem}"
    container_of = "{cont} de {elem}"

    _and_ = " et "
    and_ = "et "
    _and = " et"

    # CompOp
    is_equal_to = "est égal à"
    is_different_from = "est différent de"
    is_smaller_than = "est plus petit que"
    is_smaller_than_or_equal_to = "est plus petit que ou égal à"
    is_greater_than = "est plus grand que"
    is_greater_than_or_equal_to = "est plus grand que ou égal à"
    is_ = "est"
    is_not = "n'est pas"
    is_in = "fait partie de"
    is_not_in = "ne fait pas partie de"
    _is_between_ = " est entre "
    _inclusive = " (inclusif)"
    _exclusive = " (exclusif)"

    # Imports
    well_use = "on va utiliser {what} {names}"
    well_use_from_module = "on va utiliser {what} {names} du module {mod}"
    the_module = "le module"
    the_modules = "les modules"
    the_element = "l’élément"
    the_elements = "les éléments"
    _calling_it = " (en l’appelant {alias})"

    add_ = "ajoute "
    _to_dest = " à {dest}"
    subtract_src_ = "diminue {dest} de "
    multiply_by_ = "multiplie {dest} par "
    divide_by_ = "divise {dest} par "
    int_divide_by_ = "divise en nombres entiers {dest} par "
    store_mod_ = "dans {dest}, stocke le reste de la division de {src} par "
    store_power_ = "dans {dest}, stocke {src} à la puissance de "
    store_op_ = "dans {dest}, stocke le résultat de {src} {op} "

    the_expansion_of = "l’expansion de {expr}"

    # Constants
    empty_str = "une chaîne de caractères vide"
    something_to_be_defined = "quelque chose à définir"
    empty_value = "une valeur vide"

    # UnOp
    the_opposite_of_ = "l’opposé de "
    the_same_as_ = "le même que "
    the_logical_opposite_of_ = "le contraire de "

    # BinOp
    the_units_digit_of_ = "le chiffre des unités de "
    n_last_digits_of_ = "les {n} derniers chiffres de "
    _modulo_ = " modulo {val} (donc {desc}"
    the_sum_of_ = "la somme de "
    the_difference_between_ = "la différence entre "
    the_product_ = "le produit "
    the_quotient_of_ = "le quotient de "
    _divided_by_ = " divisé par "
    the_integer_quotient_of_ = "le quotient entier de "
    the_remainder_of_the_division_of_ = "le reste de la division de "
    _by_ = " par "
    _to_the_power_of_ = " à la puissance "
    the_result_of = "le résultat de "

    # Call
    display_empty_line = "affiche une ligne vide"
    display_ = "affiche "
    the_square_root_of_ = "la racine carrée de "
    the_rounded_value_of = "la valeur arrondie de "
    _rounded_up = " arrondi vers le haut"
    _rounded_down = " arrondi vers le bas"
    the_sine_of_ = "le sinus de "
    the_cosine_of_ = "le cosinus de "
    the_tangent_of_ = "la tangente de "
    the_user_response_to_question_ = "la réponse de l’utilisateur à la question "
    what_the_user_will_type = "ce que l’utilisateur va taper"
    the_str_conversion_of_ = "la conversion en chaîne de caractères de "
    the_float_conversion_of_ = "la conversion en nombre à virgule de "
    the_int_conversion_of_ = "la conversion en nombre entier de "
    the_bool_conversion_of_ = "la conversion en vrai/faux de "
    the_absolute_value_of_ = "la valeur absolue de "
    the_type_of_ = "le type de "
    the_length_of_ = "la longueur de "
    an_empty_list = "une liste vide"
    the_list_conversion_of_ = "la conversion en liste de "
    an_empty_set = "un ensemble vide"
    the_set_conversion_of_ = "la conversion en ensemble de "
    an_empty_tuple = "un tuple vide"
    the_tuple_conversion_of_ = "la conversion en tuple de "
    an_empty_dict = "un dictionnaire vide"
    the_dict_conversion_of_ = "la conversion en dictionnaire de "
    an_undefined_range = "une plage non définie"
    the_range_from_ = "la plage de "
    _to_ = " à "
    _with_a_step_of_ = " avec un pas de "

    _starts_with_ = " commence par "
    _ends_with_ = " finit par "
    an_uppercase_copy_of_ = "une copie tout en majuscules de "
    a_lowercase_copy_of_ = "une copie tout en minuscules de "
    a_capitalized_copy_of_ = "une copie avec la première lettre en majuscule de "
    a_titled_copy_of_ = "une copie avec la première lettre de chaque mot en majuscule de "
    a_trimmed_copy_of_ = "une copie sans espaces de début et de fin de "
    an_ltrimmed_copy_of_ = "une copie sans espaces de début de "
    an_rtrimmed_copy_of_ = "une copie sans espaces de fin de "
    at_the_end_of_ = "à la fin de "
    _append_ = ", ajoute "
    _append_elements_ = ", ajoute les éléments "
    _append_elements_of_ = ", ajoute tous les éléments de "
    at_position = "à la position "
    _in_ = " de "
    _insert_ = ", insère "
    in_ = "dans "
    _insert_undefined = ", insère quelque chose de mal défini"
    from_ = "de "
    _remove_ = ", retire "
    _remove_last_item = ", supprime le dernier élément"
    _remove_at_position_ = ", supprime l’élément à la position "
    remove_all_elements_of_ = "supprime tous les éléments de "
    index_in_ = "la position dans "
    _of_an_undefined_item = " d’un élément mal défini"
    _of_ = " de "
    _starting_at_ = " (à partir de la position "
    _between_position_ = " (entre la position "
    _and_position_ = " et la position "
    the_number_of_occurrences_in_ = "le nombre d’occurrences dans "
    sort_ = "trie "
    reverse_ = "inverse l’ordre des éléments de "
    a_copy_of_ = "une copie de "
    _add_ = ", inclus "

    call_function = "appelle la fonction {f}"
    the_result_of_function = "le résultat de la fonction {f}"
    call_method_ = "appelle la méthode {m} de "
    the_result_of_method_ = "le résultat de la méthode {m} de "
    _with_ = " avec "

    # Collections
    empty_collection = "{coll} vide"
    collection_with_one_item = "{coll} avec un seul élément"
    collection_with_items_ = "{coll} avec les éléments "
    a_list = "une liste"
    a_set = "un ensemble"
    a_tuple = "un tuple"
    an_empty_dict = "un dictionnaire vide"
    a_dict_linking_ = "un dictionnaire reliant "
    a_dict_linking_enum = "un dictionnaire reliant: "

    # Misc
    the_elements_of_ = "les éléments de "
    just_pass = "ne fais rien de spécial"

    # Control flow
    break_loop = "sors de la boucle"
    continue_loop = "passe à l’itération suivante"
    function_return = "sors de la fonction"
    function_return_value_ = "sors de la fonction en renvoyant "
    yield_none = "génère une valeur vide"
    yield_ = "génère "
    try_ = "essaie de faire ceci:"
    except_ = "en cas d’erreur:"
    finally_ = "dans tous les cas, finis par ceci:"
    try_else_ = "s’il n'y a pas eu d’erreur:"
    await_ = "attends "
    if_ = "si "
    else_comma_ = "sinon, "
    else_colon_ = "sinon:"

    # For
    repeat_as_many_times_as_elements_in_ = "répète autant de fois qu’il y a d’éléments dans "
    _counting_with_var_from_0 = " (en comptant avec {var} à partir de 0):"
    repeat_ = "répète "
    _times_details = " fois{details}"
    repeat_for_each_item_of_ = "répète pour chaque élément de "
    _which_well_call_and_number_from_ = " (qu'on va appeler {elem} et numéroter {index} depuis "
    _which_well_call = " (qu'on va appeler {elem})"
    repeat_for_each_character_in_ = 'répète pour chaque caractère dans "{str}"{details}'
    if_loop_wasnt_broken_ = "si la boucle n’a pas été interrompue:"
    repeat_indefinitely_ = "répète indéfiniment:"
    while_ = "tant que "

    # Def/lambdas
    define_function_ = "définis la fonction {name}, "
    without_argument_ = "sans argument, "
    which_accepts_one_argument_ = "qui demande un argument, "
    which_accepts_n_arguments_ = "qui demande {n} arguments"
    which_returns_nothing = "qui ne renvoie rien, "
    _which_returns_ = "qui renvoie "
    which_returns_this_ = "qui renvoie {ret}, "
    so_ = "ainsi:"
    an_anonymous_function_ = "une fonction anonyme "
    without_arguments = "sans argument"

    # Subscripts
    a_copy_of_ = "une copie de "
    the_plural_ = "les "
    _first_elements_of_ = " premiers éléments de "
    the_elements_of_ = "les éléments de "
    _starting_at_position_ = " à partir de la position "
    _from_position_ = " de la position "
    _to_position_ = " à "
    _with_one_elements_out_of = " avec un élément sur {step}"
    ith_element_of_ = "le {index}ᵉ élément de "
    the_element_at_position_ = "l’élément "

    # Conditions
    _is_true = " est vrai"
    _is_not_true = " n’est pas vrai"
    _is_false = " est faux"
    _is_not_false = " n’est pas faux"
    _and_if = " que"
    and_op = "et"
    or_op = "ou"
    _is_even = " est un nombre pair"
    _is_odd = " est un nombre impair"
    _is_multiple_of = " est un multiple de {n}"
    _is_not_multiple_of = " n’est pas un multiple de {n}"
    _is_empty = " est vide"
    _is_not_empty = " n’est pas vide"
    true_false_according_do_ = "vrai/faux selon si "

    def get_language_code(self) -> str:
        return 'fr'

    def post_process_pseudocode(self, pseudocode: str) -> str:
        return (
            pseudocode
                .replace(" à le ", " au ")
                .replace(" à les ", " aux ")
                .replace(" de les ", " des ")
                .replace(" de le ", " du ")
                .replace(" de e", " d’e")
        )
