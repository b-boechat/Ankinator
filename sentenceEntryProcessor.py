import re
from imageHandler import processImageRequest
from textFilesHandler import writeCardsToOutputFile
from getIPATranscription import getIPATranscription

def generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field):

    # Find patterns for words with no article, optionally containing a dictionary form.
    pattern_no_article = re.compile(r'\[([^\]|\d]*)(?:\|([^\]]*))?\]')
    matches_no_article = re.findall(pattern_no_article, formatted_sentence)

    #print(matches_no_article)

    #Generate fields for no-article matches.
    fields_no_article = [[
                        matches[0].lower(),  # Target, with lowercase characters.
                        getIPATranscription(matches[0].lower()),  # IPA
                        sentence,  # Sentence
                        re.sub(matches[0], "__", sentence),  # Deleted sentence
                        re.sub(matches[0], r'<span class="targetInSentence">{}</span>'.format(matches[0]), sentence),  # Sentence with HTML
                        matches[1],  # Dictionary form
                        getIPATranscription(matches[1].lower()), # Dictionary form IPA
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
                getIPATranscription(word.lower()),  # IPA
                sentence, # Sentence
                # Matches optional space character after the article, to allow both "l'xxx" and "la xxx" constructions to be formatted properly in the deleted sentence.
                re.sub(word, "__", re.sub("{} ?".format(article), "__ ", sentence)), # Deleted sentence
                re.sub(word, r'<span class="targetInSentence">{}</span>'.format(word),
                       re.sub("{} ?".format(article), r'''<span class="targetInSentence">{}</span> '''.format(article), sentence)),  # Sentence with HTML
                dictionary_form.lower(), # Dictionary form
                getIPATranscription(dictionary_form.lower()), #Dictionary form IPA
                image_field, # Image
                "" # Recording
            ])
            # Consumes tag from formatted string, so the next iteration won't find the same match.
            formatted_sentence = re.sub(number_tag, "", formatted_sentence)
    return fields_with_article

def getRawSentenceFromFormatted(formatted_sentence):
    return re.sub(r"(\[\d?)|((\|[^\]]*)?\])|(<\d?)|>", "", formatted_sentence)

def processSentenceEntry(sentence_entry):
    # Get elements from sentence entry.
    formatted_sentence, image_url = sentence_entry[0], sentence_entry[1]
    sentence = getRawSentenceFromFormatted(formatted_sentence)
    # Process the request and get image entry, if a URL was provided.
    image_field = processImageRequest(image_url, sentence)
    # Generate fields and write them to output file.
    writeCardsToOutputFile(generateAnkiFieldsNoArticle(sentence, formatted_sentence, image_field))
    writeCardsToOutputFile(generateAnkiFieldsWithArticle(sentence, formatted_sentence, image_field))