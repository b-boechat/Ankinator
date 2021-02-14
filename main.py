from sentenceEntryProcessor import processSentenceEntry
from definitions import OUTPUT_FULL_PATH, INPUT_FULL_PATH, BACKUP_PATH
from textFilesHandler import readSentencesFromInputFile, cleanOutputFile
from utilities import generateFilename
from shutil import copy2

def generateCardsFromFile(clean_output=True, backup_input=True, backup_output=True):
    sentence_entries = readSentencesFromInputFile()
    if clean_output:
        cleanOutputFile(OUTPUT_FULL_PATH)
    for entry in sentence_entries:
        processSentenceEntry(entry)

    if backup_input:
        copy2(INPUT_FULL_PATH, "{}{}.txt".format(BACKUP_PATH, generateFilename("input")))
    if backup_output:
        copy2(OUTPUT_FULL_PATH, "{}{}.txt".format(BACKUP_PATH, generateFilename("output")))


generateCardsFromFile()
