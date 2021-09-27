import csv # Write delimiter separated values
import os
import re

import regex as re

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

    if not os.path.exists(full_filepath):
        print("Couldn't find input file \"{}\"".format(full_filepath))
        raise FileNotFoundError
    # Opens input file.
    with open(full_filepath, newline="", encoding="utf-8") as input_file:
    # Reads tsv content to reader object.
        card_list_obj = csv.reader(input_file, delimiter="\t")
        # Generates list of cards.
        card_list = [row for row in card_list_obj]
    return card_list

def readSentencesFromInputFile(input_file_path, default_random_wavenet):

    if not os.path.exists(input_file_path):
        print("Couldn't find input file \"{}\"".format(input_file_path))
        raise FileNotFoundError

    # Open input file.
    with open(input_file_path, encoding="utf-8") as input_file:
        lines = list(filter(None, (line.rstrip().lstrip() for line in input_file)))
    # Initialize empty list of sentence entries.
    sentence_entries = []
    # Initialize blank sentence entry fields.
    formatted_sentence = ""
    img_url = ""
    audio_file = ""
    for line in lines:
        repl_line, match = re.subn(r"^i\s*=\s*", "", line, count=1)
        if match:
            # Line corresponds to an image url entry
            img_url = repl_line
            continue

        repl_line, match = re.subn(r"^[ar]\s*=\s*", "", line, count=1)
        if match:
            # Line corresponds to an audio file entry.
            audio_file = repl_line
            continue

        # If none of the conditions were satisfied, line corresponds to a formatted sentence entry.

        if formatted_sentence:
            if not audio_file and default_random_wavenet:
                audio_file = "tts:w."
             # If it's not the first sentence, append the previous entry to sentence entries.
            sentence_entries.append([formatted_sentence, img_url, audio_file])
            img_url = ""
            audio_file = ""
        # Save formatted sentence entry.
        formatted_sentence = repl_line

    # Append last sentence entry.
    if formatted_sentence:
        if not audio_file and default_random_wavenet:
            audio_file = "tts:w."
        sentence_entries.append([formatted_sentence, img_url, audio_file])

    return sentence_entries