import re
from imageHandler import processImageRequest
from ioFilesHandler import writeCardsToOutputFile
from addIPATranscription import addIPATranscription
from dictionaryHandler import addSortedToFlashcardDictionary

def generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field):

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
                        ""  # Recording
                        ] for matches in matches_no_article]

    return fields_no_article


def generateAnkiFieldsWithArticle(sentence, formatted_sentence, image_field):

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
                "" # Recording
            ])
            # Consumes tag from formatted string, so the next iteration won't find the same match.
            formatted_sentence = re.sub(number_tag, "", formatted_sentence)
    return fields_with_article

def getRawSentenceFromFormatted(formatted_sentence):
    return re.sub(r"(\[\d?)|((\|[^\]]*)?\])|(<\d?)|>", "", formatted_sentence)

def processAllEntries(sentence_entries, presort_dictionary):
    anki_cards_list = []
    for sentence_entry in sentence_entries:
        # Get elements from sentence entry.
        formatted_sentence, image_url = sentence_entry[0], sentence_entry[1]
        sentence = getRawSentenceFromFormatted(formatted_sentence)
        # Process the request and get image entry, if a URL was provided.
        image_field = processImageRequest(image_url, sentence)
        # Generate fields and write them to output file.
        anki_cards_list.extend(generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field))
        anki_cards_list.extend(generateAnkiFieldsWithArticle(sentence, formatted_sentence, image_field))
    # Add IPA transcription to cards.
    addIPATranscription(anki_cards_list)
    # Writes cards to output file, as tsv.
    writeCardsToOutputFile(anki_cards_list)
    # Add words to flashcard dictionary. First paramater passed is a list of all target words and their dictionary forms, if provided.
    addSortedToFlashcardDictionary([card[0] for card in anki_cards_list] + [card[5] for card in anki_cards_list if card[5]], presort_dictionary)