from bisect import bisect_left
from definitions import IPA_DICTIONARY_FULL_PATH
import colorama
import re
import csv

def get_words_from_lines(lines):
    """ Helper function that returns list of words from list of sentences. Tries to deal gracefully with apostrophes (sometimes are part of the word, sometimes are delimiters) by using the IPA tsv as reference.
    """
    with open(IPA_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8", newline="") as file:
        # Read words from IPA dictionary to a list.
        ipa_reader = csv.reader(file, delimiter="\t")
        ipa_list_words = [row[0] for row in ipa_reader]

    # Separate lines into words, at first considering that apostrophes do not delimit words (and are part of them).
    word_candidates = [re.findall(r"\b([\w'’\-]*)(?![\w'’\-])", line) for line in lines]
    # Flatten word_candidates to a list and convert all letters to lowercase.
    word_candidates = list(map(str.lower, filter(None, [candidate for sublist in word_candidates for candidate in sublist])))

    words = []
    words_after_apostrophe = []
    # Loops through candidate words.
    for candidate in word_candidates:
        if ("'" not in candidate) and ("’" not in candidate):
            # Words with no apostrophes are immediately added.
            words.append(candidate)
        else:
            index = bisect_left(ipa_list_words, candidate)
            if index != len(ipa_list_words) and ipa_list_words[index] == candidate:
                # If a word candidate with apostrophe is found in the IPA tsv, consider it to be a single word.
                words.append(candidate)
            else:
                # Otherwise, break word candidate into two words. i.e: "l'huile" is separated into "l'" and "huile"
                match = re.search(r"([^'’]*['’])(.*)", candidate)
                words.append(match.group(1))
                if match.group(2):
                    # If the word candidate ends with apostrophe, second group will be empty. Notice that, in this case, match.group(1) is the entire word candidate.
                    words.append(match.group(2))
                    # Also append it to a different list of words after apostrophe, which are treated separately when showing color coded sentences.
                    words_after_apostrophe.append(match.group(2))

    # Remove duplicates and sort list of words.
    words = list(dict.fromkeys(words))
    words.sort()

    return words, words_after_apostrophe




def searchForNewWords(dictionary_path, word_search_path, show_sentences, newline_separator):
    """ Searches WORD_SEARCH_FILE_FULL_PATH for unknown words (not already in dictionary), printing the results. If the file is a list of sentences, break them into words before searching. If show_sentences is set to True, also prints the actual sentences from the file, with each word colored according to its presence in the dictionary. This only makes sense if the file is a list of sentences (not a list of words)
    """

    colorama.init(autoreset=True)

    # Open flashcard dictionary file and save its contents to flashcard_dictionary_list.
    with open(dictionary_path, mode="r", encoding="utf-8") as dict_file:
        flashcard_dictionary_list = dict_file.readlines()
        # Removes trailing whitespace and ignores lines consisting of only whitespace (empty lines after whitespace removal).
        flashcard_dictionary_list = list(filter(None, map(str.rstrip, flashcard_dictionary_list)))
        flashcard_dictionary_list.sort()

    with open(word_search_path, mode="r", encoding="utf-8") as word_search_file:
        word_search_lines = word_search_file.readlines()

    # Call helper function to obtain list of words from lines.
    words, words_after_apostrophe = get_words_from_lines(word_search_lines)

    known_words = []
    unknown_words = []

    for word in words:
        # Gets the leftmost insertion position for word in flashcard_dictionary_list.
        insertion_point = bisect_left(flashcard_dictionary_list, word)
        # If word is already in dictionary, add it to known words.
        if insertion_point != len(flashcard_dictionary_list) and flashcard_dictionary_list[insertion_point] == word:
            known_words.append(word)
        else:
        # Otherwise, add it to unknown words.
            unknown_words.append(word)

    if newline_separator:
        # Print count and list of known words (already in dictionary), with vertical display (separate words with newline).
        print(colorama.Fore.GREEN + "\nKnown words ({}):".format(len(known_words)), end="\n\n")
        for word in known_words:
            print(colorama.Fore.GREEN + word)
        # Print count and list of unknown words (not in dictionary).
        print(colorama.Fore.RED + "\nUnknown words ({}):".format(len(unknown_words)), end="\n\n")
        for word in unknown_words:
            print(colorama.Fore.RED + word)

    else:
        # Print count and list of known words (already in dictionary), with horizontal display (separate words with comma + space).
        print(colorama.Fore.GREEN + "\nKnown words ({}):".format(len(known_words)), end="\n\n")
        for word in known_words:
            print(colorama.Fore.GREEN + word, end=", ")
        print()
        print(colorama.Fore.RED + "\nUnknown words ({}):".format(len(unknown_words)), end="\n\n")
        for word in unknown_words:
            print(colorama.Fore.RED + word, end=", ")
        print()

    if show_sentences:
        # Loops through file lines.
        for i in range(len(word_search_lines)):
            # For each known word, replace its ocurrencies in line with a green colored version of itself.
            for word in known_words:
                # Words after apostrophes allow, obviously, apostrophes to precede them.
                if word in words_after_apostrophe:
                    word_search_lines[i] = re.sub(r"(?<![\w\-])({})(?![\w'’\-])".format(word.replace("-", r"\-")),
                                                  colorama.Fore.GREEN + r"\1" + colorama.Fore.RESET,
                                                  word_search_lines[i], flags=re.I)
                else:
                    word_search_lines[i] = re.sub(r"(?<![\w'’\-])({})(?![\w'’\-])".format(word.replace("-", r"\-")),
                                              colorama.Fore.GREEN+ r"\1" + colorama.Fore.RESET,
                                              word_search_lines[i], flags=re.I)
            # For each unknown word, replace its ocurrencies in line with a red colored version of itself.
            for word in unknown_words:
                if word in words_after_apostrophe:
                    word_search_lines[i] = re.sub(r"(?<![\w\-])({})(?![\w'’\-])".format(word.replace("-", r"\-")),
                                                  colorama.Fore.RED + r"\1" + colorama.Fore.RESET,
                                                  word_search_lines[i], flags=re.I)
                else:
                    word_search_lines[i] = re.sub(r"(?<![\w'’\-])({})(?![\w'’\-])".format(word.replace("-", r"\-")),
                                              colorama.Fore.RED + r"\1" + colorama.Fore.RESET,
                                              word_search_lines[i], flags=re.I)
        print("\nSentences:\n")
        for sentence in word_search_lines:
            print(sentence, end="")
        print()