import re
import colorama
import json
import urllib.request
from mediaHandler import processMediaRequest
from ioFilesHandler import writeCardsToOutputFile
from addIPATranscription import addIPATranscription
from dictionaryHandler import addSortedToFlashcardDictionary


def generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field, audio_field):

    # Find patterns for words with no article, optionally containing a dictionary form.
    pattern_no_article = re.compile(r'\[([^\]|\d]*)(?:\|([^\]]*))?\]')
    matches_no_article = re.findall(pattern_no_article, formatted_sentence)

    #print(matches_no_article)

    #Generate fields for no-article matches.
    fields_no_article = [[
                        matches[0].lower(),  # Target, with lowercase characters.
                        "",  # IPA transcription, will be added by addIPATranscription afterwards.
                        sentence,  # Sentence
                        re.sub(matches[0], "__", sentence),  # Deleted sentence
                        re.sub(matches[0], r'<span class="targetInSentence">{}</span>'.format(matches[0]), sentence),  # Sentence with HTML
                        matches[1],  # Dictionary form
                        "", # Dictionary form IPA transcription, will be added by addIPATranscription afterwards.
                        image_field,  # Image
                        audio_field  # Recording
                        ] for matches in matches_no_article]

    return fields_no_article


def generateAnkiFieldsWithArticle(sentence, formatted_sentence, image_field, audio_field):

    # Compile regular expression to find word with article, optionally containing a dictionary form.
    pattern_with_article = re.compile(r'<(\d)([^\>]*)>.*\[\1([^\]|]*)(?:\|([^\]]*))?\]')
    # Initialize list of fields
    fields_with_article = []
    # Initializes match object with True just so that the loop executes once.
    matches_obj = True
    while matches_obj:
        # Search for pattern, storing the match object.
        matches_obj= re.search(pattern_with_article, formatted_sentence)
        if matches_obj:
            # Retrieves relevant groupings.
            number_tag = matches_obj.group(1)
            article = matches_obj.group(2)
            word = matches_obj.group(3)
            dictionary_form = matches_obj.group(4) or "" # If optional dictionary form isn't provided, defaults to an empty string.
            fields_with_article.append([
                word.lower(),  # Target
                "",  # IPA transcription, will be added by addIPATranscription afterwards.
                sentence, # Sentence
                # Matches optional space character after the article, to allow both "l'xxx" and "la xxx" constructions to be formatted properly in the deleted sentence.
                re.sub(word, "__", re.sub("{} ?".format(article), "__ ", sentence)), # Deleted sentence
                re.sub(word, r'<span class="targetInSentence">{}</span>'.format(word), re.sub(
                    "{} ?".format(article), r'''<span class="targetInSentence">{}</span> '''.format(article), sentence)),  # Sentence with HTML
                dictionary_form.lower(), # Dictionary form
                "", # Dictionary form IPA transcription, will be added by addIPATranscription afterwards.
                image_field, # Image
                audio_field # Recording
            ])
            # Consumes tag from formatted string, so the next iteration won't find the same match.
            formatted_sentence = re.sub(number_tag, "", formatted_sentence)
    return fields_with_article

def getRawSentenceFromFormatted(formatted_sentence):
    return re.sub(r"(\[\d?)|((\|[^\]]*)?\])|(<\d?)|>", "", formatted_sentence)

def addNotesToAnki(anki_cards_list, anki_deck, anki_note_type):
    # TODO: Move this function to a better suited file.
    for card in anki_cards_list:
        request_dict = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": anki_deck,
                    "modelName": anki_note_type,
                    "fields": {
                        "Target": card[0],
                        "IPA": card[1],
                        "Sentence": card[2],
                        "Deleted sentence": card[3],
                        "Sentence with HTML": card[4],
                        "Dictionary form": card[5],
                        "Dictionary form IPA": card[6],
                        "Image": card[7],
                        "Recording": card[8]
                    },
                    "options": {
                        "allowDuplicate": True
                    }
                }
            }
        }
        requestJson = json.dumps(request_dict).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
        if response['error'] is not None:
            raise Exception(response["error"])



def processAllEntries(sentence_entries, output_file_path, dictionary_file_path, presort_dictionary, add_to_anki, anki_deck, anki_note_type):
    # TODO: Change "card" nomenclature to "note".
    anki_cards_list = []
    for sentence_entry in sentence_entries:
        # Get elements from sentence entry.
        formatted_sentence, image_url, audio_file = sentence_entry[0], sentence_entry[1], sentence_entry[2]
        sentence = getRawSentenceFromFormatted(formatted_sentence)
        # Process the requests for image and audio entries, if provided.
        image_field, audio_field = processMediaRequest(image_url, audio_file, sentence)
        # Generate fields and write them to output file.
        anki_cards_list.extend(generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field, audio_field))
        anki_cards_list.extend(generateAnkiFieldsWithArticle(sentence, formatted_sentence, image_field, audio_field))
    # Add IPA transcription to cards.
    addIPATranscription(anki_cards_list)
    # Writes cards to output file, as tsv.
    writeCardsToOutputFile(anki_cards_list, output_file_path)
    if add_to_anki:
        try:
            addNotesToAnki(anki_cards_list, anki_deck, anki_note_type)
        except Exception as e:
            # TODO: Error message should include which note (or sentence) caused the error.
            print(colorama.Fore.RED + "Error adding card to Anki: \n{}.".format(repr(e)), end="\n\n")


    # Add words to flashcard dictionary. First paramater passed is a list of all target words and their dictionary forms, if provided.
    addSortedToFlashcardDictionary([card[0] for card in anki_cards_list] + [card[5] for card in anki_cards_list if card[5]], dictionary_file_path, presort_dictionary=presort_dictionary)