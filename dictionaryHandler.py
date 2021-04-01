from definitions import FLASHCARD_DICTIONARY_FULL_PATH, STAGING_FLASHCARD_DICTIONARY_FULL_PATH
from shutil import copy2
import os
from bisect import bisect_left
import colorama

def addSortedToFlashcardDictionary(words, presort_dictionary=True):
    """ Merge list of words with flashcard dictionary file while keeping it sorted and with no repeated words. If presort_dictionary is set to False, requires and assumes that flashcard dictionary file is already sorted, and operates faster.
    """
    # Open flashcard dictionary file and save its contents to flashcard_dictionary_list.
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as input_file:
        flashcard_dictionary_list = input_file.readlines()
        # Removes trailing whitespace, and ignores lines consisting of only whitespace (empty lines after whitespace removal).
        flashcard_dictionary_list = list(filter(None, map(str.rstrip, flashcard_dictionary_list)))
        # If presort_dictionary=True, sorts list.
        if presort_dictionary:
            flashcard_dictionary_list.sort()

    # Remove duplicates and sort list of words to be merged.
    words = list(dict.fromkeys(words))
    words.sort()
    insertions = []
    # Loop through list of words.
    for word in words:
        # Getsthe leftmost insertion position for word in flashcard_dictionary_list.
        insertion_point = bisect_left(flashcard_dictionary_list, word)
        # If word is already in dictionary, ignore it.
        if insertion_point != len(flashcard_dictionary_list) and flashcard_dictionary_list[insertion_point] == word:
            print(colorama.Fore.RED + "Word was already in dictionary: {}".format(word))
            continue
        # Otherwise, append tuple with word and its insertion point to the list of insertions. This insertion point is related to the original flashcard_dictionary_list, not counting insertions from previous iterations.
        insertions.append((word, insertion_point))

    # Create new flashcard dictionary file to replace the old one.
    with open(STAGING_FLASHCARD_DICTIONARY_FULL_PATH, mode="w", encoding="utf-8") as output_file:
        next_start_index = 0
        # Loop through insertion tuples.
        for insertion in insertions:
            # Add elements from flashcard_dictionary_list (original dictionary) up until insertion point.
            for i in range(next_start_index, insertion[1]):
                output_file.write("{}\n".format(flashcard_dictionary_list[i]))
            # Add insertion at the correct position.
            output_file.write("{}\n".format(insertion[0]))
            print(colorama.Fore.GREEN + "Word added to dictionary: {}".format(insertion[0]))
            # Update start index, for flashcard_dictionary_list, for the next iteration, so that each element is added once and only once.
            next_start_index = insertion[1]
        # Add remaining elements from flashcard_dictionary_list after the last insertion.
        for i in range(next_start_index, len(flashcard_dictionary_list)):
            output_file.write("{}\n".format(flashcard_dictionary_list[i]))

    # Replace old dictionary with the new one.
    copy2(STAGING_FLASHCARD_DICTIONARY_FULL_PATH, FLASHCARD_DICTIONARY_FULL_PATH)
    os.remove(STAGING_FLASHCARD_DICTIONARY_FULL_PATH)