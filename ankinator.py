import argparse
import definitions
from generateCardsFromFile import generateCardsFromFile
from mergeDictionaryInput import mergeDictionaryInput
from searchForNewWords import searchForNewWords

def generateCardsFromFileWrapper(args):
    """ Calls generateCardsFromFile with parsed arguments.
    """
    generateCardsFromFile(clean_output=args.clean_output, presort_dictionary=args.presort_dictionary,
                          backup_input="i" not in args.nobackup, backup_output="o" not in args.nobackup,
                          backup_dictionary="d" not in args.nobackup,
                          input_file_path=args.input_path, output_file_path=args.output_path,
                          dictionary_file_path=args.dictionary_path)

def mergeDictionaryInputWrapper(args):
    """ Calls mergeDictionaryInput with parsed arguments.
        """
    mergeDictionaryInput(dictionary_path=args.dictionary_path, dict_input_path=args.dict_input_path,
                         backup_dictionary="d" not in args.nobackup, backup_dict_input="i" not in args.nobackup,
                         presort_dictionary=args.presort_dictionary)

def searchForNewWordsWrapper(args):
    """ Calls searchForNewWords with parsed arguments.
        """
    searchForNewWords(dictionary_path=args.dictionary_path, word_search_path=args.word_search_path,
                      show_sentences=args.show_sentences)



# Create parser object for command line arguments.
parser = argparse.ArgumentParser(description="Automatize Anki sentence cards generation for language learning.")

subparsers = parser.add_subparsers()

# Create subparser for "generate" (calls generateCardsFromFile)
parser_generate = subparsers.add_parser("generate", aliases=["g"], help="Generate tsv with Anki cards from input file.")

parser_generate.add_argument("-i", dest="input_path", metavar="INPUT_PATH", default=definitions.INPUT_FULL_PATH,
        help="Path to input file. If not specified, defaults to INPUT_FULL_PATH in definitions.py (currently \"%(default)s\").")
parser_generate.add_argument("-o", dest="output_path", metavar="OUTPUT_PATH", default=definitions.OUTPUT_FULL_PATH,
        help="Path to output file. If not specified, defaults to OUTPUT_FILE_PATH in definitions.py (currently \"%(default)s\").")
parser_generate.add_argument("-d", dest="dictionary_path", metavar="DICTIONARY_PATH", default=definitions.FLASHCARD_DICTIONARY_FULL_PATH,
        help="Path to flashcard dictionary file. If not specified, defaults to FLASHCARD_DICTIONARY_FULL_PATH in definitions.py (currently \"%(default)s\").")
parser_generate.add_argument("-b", "--nobackup", metavar="FILES", default=[], nargs="+", choices=["i", "o", "d"],
        help="Disables backup of specified files. (i: input; o: output; d: flashcard dictionary)")
parser_generate.add_argument("-p", "--nopresort", dest="presort_dictionary", action="store_false",
        help="Disables flashcard dictionary presorting.")
parser_generate.add_argument("-c", "--noclean", dest="clean_output", action="store_false",
        help="Disables output file cleaning before execution (not recommended).") # This option is not tested.
parser_generate.set_defaults(func=generateCardsFromFileWrapper)


# Create subparser for "merge" (calls mergeDictionaryInput)
parser_merge = subparsers.add_parser("merge", aliases=["m"], help="Add words from dictionary input file to the dictionary (currently \"%(default)s\").")

parser_merge.add_argument("dict_input_path", default=definitions.FLASHCARD_DICTIONARY_INPUT_FULL_PATH, nargs="?",
        help="Path to dictionary input file. If not specified, defaults to FLASHCARD_DICTIONARY_INPUT_FULL_PATH in definitions.py (currently \"%(default)s\").")
parser_merge.add_argument("-d", dest="dictionary_path", default=definitions.FLASHCARD_DICTIONARY_FULL_PATH,
        help="Path to flashcard dictionary file. If not specified, defaults to FLASHCARD_DICTIONARY_FULL_PATH in definitions.py (currently \"%(default)s\").")
parser_merge.add_argument("-b", "--nobackup", metavar="FILES", default=[], nargs="+", choices=["i", "d"],
        help="Disables backup of specified files. (i: dictionary input; d: flashcard dictionary)")
parser_merge.add_argument("-p", "--nopresort", dest="presort_dictionary", action="store_false",
        help="Disables flashcard dictionary presorting.")
parser_merge.set_defaults(func=mergeDictionaryInputWrapper)

# Create subparser for "search" (calls searchForNewWords)
parser_search = subparsers.add_parser("search", aliases=["s"], help="Scam word search file for new words.")

parser_search.add_argument("word_search_path", default=definitions.WORD_SEARCH_FILE_FULL_PATH, nargs="?",
        help="Path to word search input file. If not specified, defaults to FLASHCARD_DICTIONARY_INPUT_FULL_PATH in definitions.py (currently \"%(default)s\").")

parser_search.add_argument("-d", dest="dictionary_path", metavar="DICTIONARY_PATH", default=definitions.FLASHCARD_DICTIONARY_FULL_PATH,
        help="Path to flashcard dictionary file. If not specified, defaults to FLASHCARD_DICTIONARY_FULL_PATH in definitions.py (currently \"%(default)s\").")
parser_search.add_argument("-s", "--sentences", dest="show_sentences", action="store_true",
        help="Enables color coded sentence displaying. This offers a good visualization if word search file is structured in sentences")
parser_search.set_defaults(func=searchForNewWordsWrapper)

# Parse arguments and execute the appropriate function
args = parser.parse_args()
args.func(args)

