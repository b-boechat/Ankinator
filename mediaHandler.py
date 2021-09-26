import requests
import shutil
import re
from PIL import Image
from math import floor
from definitions import MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, STAGING_PATH, ANKI_MEDIA_PATH, MEDIA_FILENAME_PREFIX, IMAGE_HEIGHT, DONT_MOVE_MEDIA
from utilities import generateFilename
import os
import colorama


def downloadImageFromURL(url, path, filename):
    
    # Get image extension from URL.
    extension = re.search(r"\.([a-z0-9]*)$", url).group(1)
    # Get filename with extension.
    filename_with_extension = r"{}.{}".format(filename, extension)
    # Generate full staging path.
    full_path = r"{}{}".format(path, filename_with_extension)

    # Open the URL image and fetch the stream content.
    resp = requests.get(url, stream = True, headers={'User-Agent' : r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})

    # Raise exception if the HTTP request returned an unsucessful status code.
    resp.raise_for_status()

    # In case of success, set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    
    with open(full_path,'wb') as f:
        shutil.copyfileobj(resp.raw, f)

    image = Image.open(full_path)
    # Resize downloaded image to height=IMAGE_HEIGHT, maintaining original proportions.
    resize_ratio = IMAGE_HEIGHT/image.size[1]
    image = image.resize((floor(image.size[0]*resize_ratio), IMAGE_HEIGHT))
    image.save(full_path)

    # Returns filename with extension.
    return filename_with_extension


#def moveImage(filename_with_extension, dest_path, source_path):
#    source_full_path = r"{}{}".format(source_path, filename_with_extension)
#    image = Image.open(source_full_path)
#    dest_full_path = r"{}{}".format(dest_path, filename_with_extension)
#    image.save(dest_full_path)
#    os.remove(source_full_path)

def processImageRequest(image_url, filename):

    # If no URL was providaded, returns empty string.
    if not image_url:
        return ""
    
    # Download and resize image using helper function downloadImageFromUrl()
    filename_with_extension = downloadImageFromURL(image_url, STAGING_PATH, filename)

    if not DONT_MOVE_MEDIA:
        # Move image to Anki medias folder.
        #shutil.move(r"{}{}".format(STAGING_PATH, filename_with_extension), r"{}{}".format(ANKI_MEDIA_PATH, filename_with_extension))
        source_full_path = r"{}{}".format(STAGING_PATH, filename_with_extension)
        dest_full_path = r"{}{}".format(ANKI_MEDIA_PATH, filename_with_extension)
        shutil.move(source_full_path, dest_full_path)

    # Returns image field entry.
    return r'''<img src="{}">'''.format(filename_with_extension)

#def moveMedia(filename_with_extension, dest_path, source_path):
#    source_full_path = r"{}{}".format(source_path, filename_with_extension)
#    dest_full_path = r"{}{}".format(dest_path, filename_with_extension)
#    shutil.move(source_full_path, dest_full_path)

def processAudioRequest(audio_file, filename):
    # TODO Integrate this function with Google TTS API.

    if not audio_file:
        return ""

    extension = re.search(r"\.([a-z0-9]*)$", audio_file).group(1)
    # Get filename with extension.
    filename_with_extension = r"{}.{}".format(filename, extension)

    if not DONT_MOVE_MEDIA:
        # Move audio to Anki medias folder.
        shutil.move(r"{}{}".format(STAGING_PATH, audio_file), r"{}{}".format(ANKI_MEDIA_PATH, filename_with_extension)) # TODO: Allow audio source path to be specified as command line option.

    return r"[sound:{}]".format(filename_with_extension)


def processMediaRequest(image_url, audio_file, sentence):
    colorama.init(autoreset=True)

    if not image_url and not audio_file:
        return "", ""

    # Get first alphanumeric characters from sentence, up to a maximum of MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME.
    raw_sentence = re.sub(r'\W+', '', sentence)
    num_beginning_characters = min(MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, len(raw_sentence))
    # Generate media filename.
    filename = generateFilename("{}{}".format(MEDIA_FILENAME_PREFIX, re.sub(r'\W+', '', sentence)[:num_beginning_characters]))
    try:
        image_field = processImageRequest(image_url, filename)
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED + "Couldn't download image for sentence: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        image_field = ""

    try:
        audio_field = processAudioRequest(audio_file, filename)
    except shutil.Error as e:
        print(colorama.Fore.RED + "Error processing audio entry: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        audio_field = ""

    return image_field, audio_field




