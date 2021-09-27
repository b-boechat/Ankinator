from ioFilesHandler import readCardsFromTSV
from sentenceEntryProcessor import addNotesToAnki

def addNotesToAnkiFromTsv(file_path, anki_deck, anki_note_type):

    anki_cards_list = readCardsFromTSV(file_path)
    addNotesToAnki(anki_cards_list, anki_deck, anki_note_type)

