from sentenceEntryProcessor import processAllEntries
from ioFilesHandler import readSentencesFromInputFile, removeFile
from utilities import backupFile, displayFlagReminders

def generateCardsFromFile(clean_output,  presort_dictionary,
                          backup_input, backup_output, backup_dictionary,
                          input_file_path, output_file_path, dictionary_file_path,
                          default_recording,
                          add_to_anki, anki_deck, anki_note_type):

    displayFlagReminders()

    if backup_input:
        backupFile(input_file_path, "input")
    if backup_dictionary:
        backupFile(dictionary_file_path, "dictionary")

    sentence_entries = readSentencesFromInputFile(input_file_path, default_recording)

    if clean_output:
        removeFile(output_file_path)

    processAllEntries(sentence_entries,
                      output_file_path, dictionary_file_path,
                      presort_dictionary=presort_dictionary,
                      add_to_anki=add_to_anki, anki_deck=anki_deck, anki_note_type=anki_note_type)

    if backup_output:
        backupFile(output_file_path, "output")


