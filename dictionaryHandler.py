from definitions import FLASHCARD_DICTIONARY_FULL_PATH, STAGING_FLASHCARD_DICTIONARY_FULL_PATH
from shutil import copy2
import os
import re

def addSortedToFlashcardDictionary(word):
    # Assumes flashcard dictionary is alphabetically sorted, and adds word to it.
    was_written = False
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as input_file:
        with open(STAGING_FLASHCARD_DICTIONARY_FULL_PATH, mode="w", encoding="utf-8") as output_file:
            for line in input_file:
                # Ignores and removes empty lines from dictionary.
                if line == "\n":
                    continue
                # Repeated words are not added.
                if line.rstrip() == word:
                    was_written = True
                # Writes at the correct position.
                if not was_written and line > word:
                    output_file.write("{}\n".format(word))
                    was_written = True
                output_file.write(line)
            if not was_written:
                output_file.write("{}\n".format(word))
    copy2(STAGING_FLASHCARD_DICTIONARY_FULL_PATH, FLASHCARD_DICTIONARY_FULL_PATH)
    os.remove(STAGING_FLASHCARD_DICTIONARY_FULL_PATH)

def sortFlashcardDictionary():
    # Sorts dictionary.
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = list(filter(lambda x: not re.match(r'^\s*$', x), lines))
        lines.sort()
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="w", encoding="utf-8") as file:
        file.writelines(lines)



