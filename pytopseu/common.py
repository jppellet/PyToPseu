
# Imports

from dataclasses import dataclass

from .pseudocode_dictionary import PseudocodeDictionary
from .english_pseudocode_dictionary import EnglishPseudocodeDictionary
from .french_pseudocode_dictionary import FrenchPseudocodeDictionary

# Constants

MAX_LINE_WIDTH = 60
V_BAR = "│"
PYTHON_ANN_SEP = "#" + V_BAR
CONTINUATION_MARK = "└╴"
PREAMBLE_LENGTH = 4
MIN_CODE_WIDTH = 25

# Class Definitions

@dataclass
class PseudocodeFormat:
    file_extension: str

# Global Variables

language_pseudocode_dictionaries = {
    'en': EnglishPseudocodeDictionary(),
    'fr': FrenchPseudocodeDictionary()
}

text_pseudocode_format = PseudocodeFormat('.txt')
markdown_pseudocode_format = PseudocodeFormat('.md')
python_pseudocode_format = PseudocodeFormat('.py')

# Functions

def get_supported_languages():
    return list(language_pseudocode_dictionaries.keys())

def code_has_preamble(
    code_lines: list[str],
    pseudocode_dictionary: PseudocodeDictionary
) -> bool:
    return len(code_lines) >= PREAMBLE_LENGTH and \
        code_lines[0].startswith('"""') and \
        code_lines[PREAMBLE_LENGTH - 1].startswith('"""') and \
        code_lines[2].startswith("———") and \
        code_lines[1].startswith(pseudocode_dictionary.Code)

def strip_line_annotations(line: str) -> str:
    return line.split(PYTHON_ANN_SEP, 1)[0].rstrip()

def strip_annotations(
    code: str,
    pseudocode_dictionary: PseudocodeDictionary
) -> str:
    lines = code.split('\n')

    if code_has_preamble(lines, pseudocode_dictionary):
        lines = lines[PREAMBLE_LENGTH:]

    lines = list(map(strip_line_annotations, lines))

    return '\n'.join(lines)
