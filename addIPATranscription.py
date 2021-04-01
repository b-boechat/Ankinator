import csv
import colorama
from definitions import IPA_DICTIONARY_FULL_PATH
from bisect import bisect_left

def addIPATranscription(anki_cards_list):
    """ Add IPA transcription to list of Anki Cards created by processSentenceEntries().
    """
    # Open IPA transcriptions tsv file.
    with open(IPA_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8", newline="") as file:
        ipa_reader = csv.reader(file, delimiter="\t")
        # Generate list of entries from csv reader iterator. Each entry is two-dimensional, first element corresponds to word and second element corresponds to transcription.
        ipa_list = [row for row in ipa_reader]
        # List of words are obtained so they can be used by the bisect_left function. In the future, a binary search can be implemented to work directly with ipa_list.
        ipa_list_words = [row[0] for row in ipa_list]

    for card in anki_cards_list:
        # Use bisect_left to find index for target word in the IPA tsv.
        index = bisect_left(ipa_list_words, card[0])
        if index != len(ipa_list_words) and ipa_list_words[index] == card[0]:
            card[1] = ipa_list[index][1]
        else:
            # Word was not found in the IPA tsv.
            card[1] = "" # Should be already an empty string, reassigned here for clarity.
            print("Did not find IPA transcription for: {}".format(card[0]))

        # If dictionary form was provided, repeat the same process to find its IPA transcription. If not provided, it defaults to an empty string, so this won't get executed.
        if card[5]:
            index = bisect_left(ipa_list_words, card[5])
            if index != len(ipa_list_words) and ipa_list_words[index] == card[5]:
                card[6] = ipa_list[index][1]
            else:
                card[6] = "" # Should be already an empty string, reassigned here for clarity.
                print("Did not find IPA transcription for: {}".format(card[5]))
        else:
            card[6] = "" # Should be already an empty string, reassigned here for clarity.