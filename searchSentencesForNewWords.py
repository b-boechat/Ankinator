# Não escrito ainda.

import colorama
from definitions import FLASHCARD_DICTIONARY_FULL_PATH

print(colorama.Fore.BLUE + "Hello World")

def searchSentencesForNewWords(file_full_path):
    with open(file_full_path, mode="r", encoding="utf-8") as sentences_file:
        sentences = list(filter(None, (line.rstrip() for line in sentences_file)))
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as dictionary: