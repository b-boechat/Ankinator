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

    if not os.path.exists(full_filepath):
        print("Couldn't find input file \"{}\"".format(full_filepath))
        raise FileNotFoundError
    # Opens input file.
    with open(full_filepath, newline="") as input_file:
    # Reads tsv content to reader object.
        card_list_obj = csv.reader(input_file, delimiter="\t")
        # Generates list of cards.
        card_list = [row for row in card_list_obj]
    return card_list

def readSentencesFromInputFile(input_file_path):

    if not os.path.exists(input_file_path):
        print("Couldn't find input file \"{}\"".format(input_file_path))
        raise FileNotFoundError

    # Open input file.
    with open(input_file_path, encoding="utf-8") as input_file:
        lines = list(filter(None, (line.rstrip() for line in input_file)))

    # Initialize empty list of sentence entries.
    sentence_entries = []

    # Initialize blank sentence entry fields.
    formatted_sentence = ""
    img_url = ""
    audio_file = ""

    for line in lines:
        if line.startswith("i="):
            img_url = line[2:].lstrip()
        elif line.startswith("a="):
            audio_file = line[2:].lstrip()
        else:
            if formatted_sentence:
                sentence_entries.append([formatted_sentence, img_url, audio_file])
                img_url = ""
                audio_file = ""
            formatted_sentence = line[:]

    if formatted_sentence:
        sentence_entries.append([formatted_sentence, img_url, audio_file])


    return sentence_entries