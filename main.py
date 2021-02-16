from sentenceEntryProcessor import processSentenceEntry
from definitions import OUTPUT_FULL_PATH, INPUT_FULL_PATH, FLASHCARD_DICTIONARY_FULL_PATH
from ioFilesHandler import readSentencesFromInputFile, cleanOutputFile
from dictionaryHandler import sortFlashcardDictionary
from utilities import generateFilename, backupFile
from shutil import copy2

def generateCardsFromFile(clean_output=True, backup_input=True, backup_output=True, backup_dictionary=True, presort_dictionary=True):
    if backup_input:
        backupFile(INPUT_FULL_PATH, "input")
    if backup_dictionary:
        backupFile(FLASHCARD_DICTIONARY_FULL_PATH, "dictionary")
    if presort_dictionary:
        sortFlashcardDictionary()
    sentence_entries = readSentencesFromInputFile()
    if clean_output:
        cleanOutputFile(OUTPUT_FULL_PATH)
    for entry in sentence_entries:
        processSentenceEntry(entry)
    if backup_output:
        backupFile(OUTPUT_FULL_PATH, "output")


generateCardsFromFile()
