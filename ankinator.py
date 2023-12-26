import argparse
import definitions
from generateCardsFromFile import generateCardsFromFile
from mergeDictionaryInput import mergeDictionaryInput
from searchForNewWords import searchForNewWords
from addNotesToAnkiFromTsv import addNotesToAnkiFromTsv

def generateCardsFromFileWrapper(args):
    """ Calls generateCardsFromFile with parsed arguments.
    """
    generateCardsFromFile(clean_output=args.clean_output, presort_dictionary=args.presort_dictionary,
                          backup_input="i" not in args.nobackup, backup_output="o" not in args.nobackup,
                          backup_dictionary="d" not in args.nobackup,
                          input_file_path=args.input_path, output_file_path=args.output_path,
                          dictionary_file_path=args.dictionary_path,
                          default_recording=args.default_recording,
                          add_to_anki=args.add_to_anki, anki_deck=args.anki_deck, anki_note_type = args.anki_note_type
                          )

def mergeDictionaryInputWrapper(args):
    """ Calls mergeDictionaryInput with parsed arguments.
        """
    mergeDictionaryInput(dictionary_path=args.dictionary_path, dict_input_path=args.dict_input_path,
                         backup_dictionary="d" not in args.nobackup, backup_dict_input="i" not in args.nobackup,
                         presort_dictionary=args.presort_dictionary
                         )

def searchForNewWordsWrapper(args):
    """ Calls searchForNewWords with parsed arguments.
        """
    searchForNewWords(dictionary_path=args.dictionary_path, word_search_path=args.word_search_path,
                      show_sentences=args.show_sentences, newline_separator=args.newline_separator
                      )

def addNotesToAnkiFromTsvWrapper(args):
    """ Calls addNotesToAnki with parsed arguments.
        """
    addNotesToAnkiFromTsv(file_path=args.file_path,
                   anki_deck=args.anki_deck, anki_note_type=args.anki_note_type
                   )



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
        help="Disables output file cleaning before execution (not recommended).") # TODO: Tests needed.
#parser_generate.add_argument("-r", "--defaultrandomwavenet", dest="default_random_wavenet", action="store_true",
#        help="If audio request is not specified, defaults to a random Google TTS Wavenet voice.")
parser_generate.add_argument("-r", "--defaultrecording", dest="default_recording", choices=["w", "s", "n"], default="s",
        help="Specifies default recording type if audio entry is not provided. (w: random Google TTS FR/FR Wavenet voice; s: random Google TTS FR/FR Studio voice; n: none)")
parser_generate.add_argument("-a", "--addtoanki", dest="add_to_anki", action="store_true",
        help="Enables adding generated flashcards directly to Anki. Additional arguments --deck and --type can be specified.")
parser_generate.add_argument("-e", "--deck", dest="anki_deck", metavar="ANKI_DECK", default=definitions.ANKI_DECK,
        help="Anki deck name. Only useful alongside --addtoanki. If not specified, defaults to ANKI_DECK in definitions.py (currently \"%(default)s\").")
parser_generate.add_argument("-t", "--type", dest="anki_note_type", metavar="ANKI_NOTE_TYPE", default=definitions.ANKI_NOTE_TYPE,
        help="Anki note type name. Only useful alongside --addtoanki. If not specified, defaults to ANKI_NOTE_TYPE in definitions.py (currently \"%(default)s\").")
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
parser_search.add_argument("-n", "--newline", dest="newline_separator", action="store_true",
        help="Display lists of known and unknown words separated with newline, instead of comma + space.")
parser_search.set_defaults(func=searchForNewWordsWrapper)


# Create subparser for "generate" (calls generateCardsFromFile)
parser_add = subparsers.add_parser("add", aliases=["a"], help="Add notes to Anki from TSV file.")

parser_add.add_argument("-f", dest="file_path", metavar="FILE_PATH", default=definitions.OUTPUT_FULL_PATH,
        help="Path to tsv file. If not specified, defaults to OUTPUT_FILE_PATH in definitions.py (currently \"%(default)s\").")
parser_add.add_argument("-e", "--deck", dest="anki_deck", metavar="ANKI_DECK", default=definitions.ANKI_DECK,
        help="Anki deck name. If not specified, defaults to ANKI_DECK in definitions.py (currently \"%(default)s\").")
parser_add.add_argument("-t", "--type", dest="anki_note_type", metavar="ANKI_NOTE_TYPE", default=definitions.ANKI_NOTE_TYPE,
        help="Anki note type name. If not specified, defaults to ANKI_NOTE_TYPE in definitions.py (currently \"%(default)s\").")
parser_add.set_defaults(func=addNotesToAnkiFromTsvWrapper)


# Parse arguments and execute the appropriate function, or show usage message if program was called without arguments.
args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_usage()

