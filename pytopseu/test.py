
# Imports

import os
import sys

from .common import *
from .dictionaries.pseudocode_dictionary import PseudocodeDictionary
from .pytopseu import annotate_code

# Constants

INPUT_FOLDER = "sample_src/input"
OUTPUT_FOLDER = "sample_src/output"
ANNOTATED_SUFFIX = "_ann.py"

# Functions

def annotate_file_for_all_supported_languages(file, pseudocode_format):
    for lang in get_supported_languages():
        annotate_file(file, pseudocode_format, language_pseudocode_dictionaries[lang])

def annotate_file(
    file: str,
    pseudocode_format: PseudocodeFormat,
    pseudocode_dictionary: PseudocodeDictionary,
    dump_ast: bool = False
) -> None:
    lang = pseudocode_dictionary.get_language_code()
    print(f"Processing '{file}' in lang={lang}")

    with open(file, "r", encoding="utf8") as source_file:
        source = source_file.read()

    annotated = annotate_code(
        source,
        pseudocode_format,
        pseudocode_dictionary,
        underline_variable_names=True,
        dump_ast=dump_ast
    )
    if not annotated:
        print("Syntax error")
        return

    file_extension = pseudocode_format.file_extension

    if pseudocode_format == python_pseudocode_format:
        file_extension = ANNOTATED_SUFFIX

    current_filename = os.path.split(file)[1]
    current_filename_base = os.path.splitext(current_filename)[0]
    outfile = os.path.join(OUTPUT_FOLDER, current_filename_base + "_" + lang + file_extension)

    with open(outfile, "w", encoding="utf8") as out_file:
        out_file.write("\n".join(annotated.output))

    print(f"Output written to '{outfile}'\n")


def annotate_all(format: PseudocodeFormat) -> None:
    for file in sorted(os.listdir(INPUT_FOLDER)):
        if file.endswith(PYTHON_EXTENSION) and not file.endswith(ANNOTATED_SUFFIX):
            for lang in get_supported_languages():
                annotate_file(
                    os.path.join(INPUT_FOLDER, file),
                    format,
                    language_pseudocode_dictionaries[lang]
                )

# Execution

file = sys.argv[1] if len(sys.argv) > 1 else None

if file:
    annotate_file_for_all_supported_languages(file, python_pseudocode_format)
else:
    annotate_all(python_pseudocode_format)
