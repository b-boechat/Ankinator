import csv # Write delimiter separated values
import os

def removeFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def writeCardsToOutputFile(card_list, output_file_path):
    #Open output file
    with open(output_file_path, "at", newline="", encoding="utf-8") as output_file:
        #Appends contents from card_list as tab separated values.
        tsv_writer = csv.writer(output_file, delimiter="\t")
        for card in card_list:
            tsv_writer.writerow(card)

def readCardsFromTSV(full_filepath):
    # This function is just for debugging purposes.

    # Opens input file.
    with open(full_filepath, newline="") as input_file:
    # Reads tsv content to reader object.
        card_list_obj = csv.reader(input_file, delimiter="\t")
        # Generates list of cards.
        card_list = [row for row in card_list_obj]
    return card_list

def readSentencesFromInputFile(input_file_path):
    # Open input file.
    with open(input_file_path, encoding="utf-8") as input_file:
        lines = list(filter(None, (line.rstrip() for line in input_file)))
    # Assert proper format (formatted sentence, url link or .)
    assert (len(lines) % 2 == 0)
    # Generate list of sentence entries.
    sentence_entries = []
    for i in range(0, len(lines), 2):
        # If image url line is "." (means not provided), change "." to empty string.
        if lines[i+1] == ".":
            lines[i+1] = ""
        sentence_entries.append([lines[i], lines[i+1]])

    return sentence_entries

