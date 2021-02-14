from sentenceEntryProcessor import *
from imageHandler import *
from getIPATranscription import *
from definitions import *
from utilities import *
from textFilesHandler import *

formatted_sentence = r"Je sais: ça [ressembler] [énormément] à <1un> [1supplice]."

print(getRawSentenceFromFormatted(formatted_sentence))

