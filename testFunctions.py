from sentenceEntryProcessor import *
from main import *
from imageHandler import *
from getIPATranscription import *
from definitions import *
from utilities import *
from textFilesHandler import *

# Define sentence and formatted string to be processed.
sentence = "J'ai peur de tomber de l'echelle."
formatted_string = "J'ai [peur] de [tomber] de <1l'>[1echelle]."
filepath = "files/output.txt"

fields_no_article = generateAnkiFieldsNoArticle(sentence, formatted_string)
#print(fields_no_article)

sentence_entries = readSentencesFromFile("files/input.txt")

print(sentence_entries)


fields_with_article = generateAnkiFieldsWithArticle(sentence, formatted_string)
#print(fields_with_article)

cleanOutputFile(filepath)
writeCardsAsTSV(filepath, fields_no_article)
writeCardsAsTSV(filepath, fields_with_article)

#print("")
#print(readCardsFromTSV(filepath))

