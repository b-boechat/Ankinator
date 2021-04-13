from dictionaryHandler import addSortedToFlashcardDictionary
from utilities import backupFile, displayFlagReminders


def mergeDictionaryInput(dictionary_path, dict_input_path,
                         backup_dictionary, backup_dict_input,
                         presort_dictionary):
    """ Merges dictionary input file with dictionary, ignoring repeated words and adding new words sorted and all lowercase. If presort_dictionary is set to False, requires and assumes that flashcard dictionary file is already sorted, and operates faster.
    """

    displayFlagReminders(dont_move_images_reminder=False)

    if backup_dictionary:
        backupFile(dictionary_path, "dictionary")

    if backup_dict_input:
        backupFile(dict_input_path, "dict_input")

    if not os.path.exists(dict_input_path):
        print("Couldn't find dictionary input file \"{}\"".format(dict_input_path))
        raise FileNotFoundError

    with open(dict_input_path, mode="r", encoding="utf-8") as input_file:
        input_list = input_file.readlines()
        input_list = list(filter(None, map(str.rstrip, map(str.lower, input_list))))


    addSortedToFlashcardDictionary(input_list, dictionary_path, presort_dictionary)
