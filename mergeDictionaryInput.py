from definitions import FLASHCARD_DICTIONARY_FULL_PATH, FLASHCARD_DICTIONARY_INPUT_FULL_PATH
from dictionaryHandler import addSortedToFlashcardDictionary
from utilities import backupFile


def mergeDictionaryInput(backup_dictionary=True, backup_dictionary_input=True, presort_dictionary=True):
    """ Merges dictionary input file with dictionary, ignoring repeated words and adding new words sorted and all lowercase. If presort_dictionary is set to False, requires and assumes that flashcard dictionary file is already sorted, and operates faster.
    """
    if backup_dictionary:
        backupFile(FLASHCARD_DICTIONARY_FULL_PATH, "dictionary")

    if backup_dictionary_input:
        backupFile(FLASHCARD_DICTIONARY_FULL_PATH, "dict_input")

    with open(FLASHCARD_DICTIONARY_INPUT_FULL_PATH, mode="r", encoding="utf-8") as input_file:
        input_list = input_file.readlines()
        input_list = list(filter(None, map(str.rstrip, map(str.lower, input_list))))


    addSortedToFlashcardDictionary(input_list, presort_dictionary)


mergeDictionaryInput()
