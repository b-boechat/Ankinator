from sentenceEntryProcessor import processAllEntries
from definitions import OUTPUT_FULL_PATH, INPUT_FULL_PATH, FLASHCARD_DICTIONARY_FULL_PATH
from ioFilesHandler import readSentencesFromInputFile, cleanOutputFile
from utilities import backupFile, displayFlagReminders

def generateCardsFromFile(clean_output=True, backup_input=True, backup_output=True, backup_dictionary=True, presort_dictionary=True):

    displayFlagReminders()

    if backup_input:
        backupFile(INPUT_FULL_PATH, "input")
    if backup_dictionary:
        backupFile(FLASHCARD_DICTIONARY_FULL_PATH, "dictionary")
    sentence_entries = readSentencesFromInputFile()
    if clean_output:
        cleanOutputFile(OUTPUT_FULL_PATH)

    processAllEntries(sentence_entries, presort_dictionary)

    if backup_output:
        backupFile(OUTPUT_FULL_PATH, "output")


generateCardsFromFile()

