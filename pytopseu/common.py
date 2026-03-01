
# Imports

from dataclasses import dataclass

from .english_pseudocode_dictionary import EnglishPseudocodeDictionary
from .french_pseudocode_dictionary import FrenchPseudocodeDictionary

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
