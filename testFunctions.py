from sentenceEntryProcessor import *
from imageHandler import *
from addIPATranscription import *
from definitions import *
from utilities import *
from ioFilesHandler import *
from dictionaryHandler import *

#formatted_sentence = r"Je sais: ça [ressembler] [énormément] à <1un> [1supplice]."

#print(getRawSentenceFromFormatted(formatted_sentence))


addSortedToFlashcardDictionary("kappa")
addSortedToFlashcardDictionary("abelha")
addSortedToFlashcardDictionary("ola")
addSortedToFlashcardDictionary("banana")

sortFlashcardDictionary()