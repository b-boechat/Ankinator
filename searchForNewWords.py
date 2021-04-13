from bisect import bisect_left
from definitions import IPA_DICTIONARY_FULL_PATH
import colorama
import regex as re
import csv

def get_words_from_lines(lines):
    """ Helper function that returns list of words from list of sentences. Tries to deal gracefully with apostrophes (which are sometimes part of the word and sometimes delimeters) by using the IPA tsv as reference. Return value has words in the same order as originally in the text, including duplicates.
    """
    with open(IPA_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8", newline="") as file:
        # Read words from IPA dictionary to a list.
        ipa_reader = csv.reader(file, delimiter="\t")
        ipa_list_words = [row[0] for row in ipa_reader]

    # Separate lines into words, at first considering that apostrophes do not delimit words (and are part of them).
    word_candidates = [re.findall(r"\b([\p{L}'’\-]*)(?![\p{L}'’\-])", line) for line in lines]
    # Flatten word_candidates to a list and convert all letters to lowercase.

    word_candidates = list(map(str.lower, filter(None, [candidate for sublist in word_candidates for candidate in sublist])))

    words = []
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

    return words

def searchForNewWords(dictionary_path, word_search_path, show_sentences, newline_separator):
    """ Searches WORD_SEARCH_FILE_FULL_PATH for unknown words (not already in dictionary), printing the results. If the file is a list of sentences, break them into words before searching. If show_sentences is set to True, also prints the actual sentences from the file, with each word colored according to its presence in the dictionary. This only makes sense if the file is a list of sentences (not a list of words)
    """

    colorama.init(autoreset=True)

    print("Scanning file {} for words...".format(word_search_path))

    # Open flashcard dictionary file and save its contents to flashcard_dictionary_list.
    with open(dictionary_path, mode="r", encoding="utf-8") as dict_file:
        flashcard_dictionary_list = dict_file.readlines()
        # Remove trailing whitespace and ignores lines consisting of only whitespace (empty lines after whitespace removal).
        flashcard_dictionary_list = list(filter(None, map(str.rstrip, flashcard_dictionary_list)))
        flashcard_dictionary_list.sort()

    with open(word_search_path, mode="r", encoding="utf-8") as word_search_file:
        word_search_lines = word_search_file.readlines()
        # Remove indicator character ϰ, if it occurs in the text (unlikely). This situation is not ideal, but better than breaking the show_sentence code (see below).
        for i in range(len(word_search_lines)):
            word_search_lines[i] = re.sub(r"ϰ", "", word_search_lines[i])

    # Call helper function to obtain list of words from lines.
    words = get_words_from_lines(word_search_lines)

    # Generate list of words with no duplicates and sorted. The original "words" variable is not changed, as it's still needed.
    unique_words = list(dict.fromkeys(words))
    unique_words.sort()

    known_words = []
    unknown_words = []

    for word in unique_words:
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
        print("\nKnown words ({}):".format(len(known_words)), end="\n\n")
        for word in known_words:
            print(colorama.Fore.GREEN + word)
        # Print count and list of unknown words (not in dictionary).
        print("\nUnknown words ({}):".format(len(unknown_words)), end="\n\n")
        for word in unknown_words:
            print(colorama.Fore.RED + word)

    else:
        # Print count and list of known words (already in dictionary), with horizontal display (separate words with comma + space).
        print("\nKnown words ({}):".format(len(known_words)), end="\n\n")
        for word in known_words:
            print(colorama.Fore.GREEN + word, end=", ")
        print()
        print("\nUnknown words ({}):".format(len(unknown_words)), end="\n\n")
        for word in unknown_words:
            print(colorama.Fore.RED + word, end=", ")
        print()

    if show_sentences:
        # Initialize index to traverse word_search_lines
        i = 0
        for word in words:
            # Set match_num to 0, just to execute the while loop at least once for each word.
            match_num = 0
            while not match_num:
                # Try to find a match for current word in current (i-th) line. Only one match is made, since count is set to 1.
                # Replace match with colored version followed by special character ϰ, which indicates that this portion of the string has been consumed. The regex does not match if there's a ϰ character somewhere ahead in the string.
                # If match is successful, match_num is set to 1, and the loop breaks. Otherwise, match_num is set to 0.
                word_search_lines[i], match_num = re.subn(r"({})(?![^ϰ]+ϰ)".format(word.replace("-", r"\-")),
                        (colorama.Fore.GREEN if word in known_words else colorama.Fore.RED)+r"\1"+colorama.Fore.RESET+"ϰ",
                        word_search_lines[i], count=1, flags=re.I)
                if not match_num:
                # If no match is found, increment i, so the next iteration will search in the next line.
                    i += 1
                    # This exception should never be raised, it's here for safety (to avoid infinite looping if there's a bug in the code).
                    if i >= len(word_search_lines):
                        raise Exception
        # Remove indicator characters.
        for i in range(len(word_search_lines)):
            word_search_lines[i] = re.sub(r"ϰ", "", word_search_lines[i])



        print("\nText:\n")
        for sentence in word_search_lines:
            print(sentence, end="")
        print()