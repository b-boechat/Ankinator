import csv # Write delimiter separated values
import os
from definitions import *

def cleanOutputFile(full_filepath):
    if os.path.exists(full_filepath):
        os.remove(full_filepath)

def writeCardsToOutputFile(card_list):
    #Open output file
    with open(OUTPUT_FULL_PATH, "at", newline="", encoding="utf-8") as output_file:
        #Appends contents from card_list as tab separated values.
        tsv_writer = csv.writer(output_file, delimiter="\t")
        for card in card_list:
            tsv_writer.writerow(card)

def readCardsFromTSV(full_filepath):
    # This function is just for debugging purposes.

    # Opens input file.
    input_file = open(full_filepath, newline="")
    # Reads tsv content to reader object.
    card_list_obj = csv.reader(input_file, delimiter="\t")
    # Generates list of cards.
    card_list = [row for row in card_list_obj]
    input_file.close()
    return card_list

def readSentencesFromInputFile():
    # Open input file.
    with open(INPUT_FULL_PATH, encoding="utf-8") as input_file:
        lines = list(filter(None, (line.rstrip() for line in input_file)))
    # Assert proper format (sentence, formatted sentence, url link or .)
    assert (len(lines) % 3 == 0)
    # Generate list of sentence entries.
    sentence_entries = []
    for i in range(0, len(lines), 3):
        # If image url line is "." (means not provided), change "." to empty string.
        if lines[i+2] == ".":
            lines[i+2] = ""
        sentence_entries.append([lines[i], lines[i+1], lines[i+2]])

    return sentence_entries

