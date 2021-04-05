from definitions import FLASHCARD_DICTIONARY_FULL_PATH, WORD_SEARCH_FILE_FULL_PATH
from bisect import bisect_left
import colorama
import re
import sys

def replace_with_colored(match_obj, color):
    """ Helper function that returns colored word."""
    return color + match_obj.group(1) + colorama.Fore.RESET + match_obj.group(2)

def searchForNewWords(show_sentences=False):
    """ Searches WORD_SEARCH_FILE_FULL_PATH for unknown words (not already in dictionary), printing the results. If the file is a list of sentences, break them into words before searching. If show_sentences is set to True, also prints the actual sentences from the file, with each word colored according to its presence in the dictionary. This only makes sense if the file is a list of sentences (not a list of words)
    """

    colorama.init(autoreset=True)

    # Open flashcard dictionary file and save its contents to flashcard_dictionary_list.
    with open(FLASHCARD_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as dict_file:
        flashcard_dictionary_list = dict_file.readlines()
        # Removes trailing whitespace and ignores lines consisting of only whitespace (empty lines after whitespace removal).
        flashcard_dictionary_list = list(filter(None, map(str.rstrip, flashcard_dictionary_list)))
        flashcard_dictionary_list.sort()

    with open(WORD_SEARCH_FILE_FULL_PATH, mode="r", encoding="utf-8") as word_search_file:
        word_search_lines = word_search_file.readlines()
        # Removes trailing whitespace and ignores only whitespace lines.
        words = filter(None, map(str.lower, map(str.rstrip, word_search_lines)))
        # Split into separate words and flatten the list.
        words = map(str.split, words)
        words = [word for sublist in words for word in sublist]
        words = list(map(lambda string: string.rstrip(".,; "), words))

    # Remove duplicates and sort list of words.
    words = list(dict.fromkeys(words))
    words.sort()

    known_words = []
    unknown_words = []

    for word in words:
        # Gets the leftmost insertion position for word in flashcard_dictionary_list.
        insertion_point = bisect_left(flashcard_dictionary_list, word)
        # If word is already in dictionary, ignore it.
        if insertion_point != len(flashcard_dictionary_list) and flashcard_dictionary_list[insertion_point] == word:
            known_words.append(word)
        else:
            unknown_words.append(word)
        if "'" in word:
            print(colorama.Fore.YELLOW + "Apostrophe warning: {}".format(word))

    # Print count and list of known words (already in dictionary).
    print(colorama.Fore.GREEN + "\nKnown words ({}):".format(len(known_words)), end="\n\n")
    for word in known_words:
        print(colorama.Fore.GREEN + word)
    # Print count and list of unknown words (not in dictionary).
    print(colorama.Fore.RED + "\nUnknown words ({}):".format(len(unknown_words)), end="\n\n")
    for word in unknown_words:
        print(colorama.Fore.RED + word)

    if show_sentences:
        for i in range(len(word_search_lines)):
            for word in known_words:
                word_search_lines[i] = re.sub("({})([\s,.;])".format(word), lambda match_obj : replace_with_colored(match_obj, colorama.Fore.GREEN), word_search_lines[i])
            for word in unknown_words:
                word_search_lines[i] = re.sub("({})([\s,.;])".format(word), lambda match_obj : replace_with_colored(match_obj, colorama.Fore.RED), word_search_lines[i])
        print("\nSentences:\n")
        for sentence in word_search_lines:
            print(sentence, end="")
        print()


if len(sys.argv) == 2 and sys.argv[1] == "-s":
    searchForNewWords(show_sentences=True)
else:
    searchForNewWords()