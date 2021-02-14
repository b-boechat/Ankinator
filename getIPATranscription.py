import re
from definitions import IPA_DICTIONARY_FULL_PATH

def getIPATranscription(key):
    # Very lazy implementation, binary search should be used.

    if not key:
        return ""
    with open(IPA_DICTIONARY_FULL_PATH, mode="r", encoding="utf-8") as file:
        contents = file.read()
        ipa_match = re.search(r"\n{}\t/([^/]*)/".format(key), contents)
        if not ipa_match:
            print("IPA transcript for \"{}\" not found.".format(key))
            return ""

    return ipa_match.group(1)