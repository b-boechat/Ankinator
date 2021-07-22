import requests
import shutil
import re
from PIL import Image
from math import floor
from definitions import MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, STAGING_PATH, IMAGE_PATH, IMAGE_FILENAME_PREFIX, IMAGE_HEIGHT, DONT_MOVE_IMAGES
from utilities import generateFilename
import os
import colorama


def downloadImageFromURL(url, path, filename):
    
    # Get image extension from URL.
    extension = re.search(r"\.([a-z]*)$", url).group(1)
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


def moveImage(filename_with_extension, dest_path, source_path):
    source_full_path = r"{}{}".format(source_path, filename_with_extension)
    image = Image.open(source_full_path)
    dest_full_path = r"{}{}".format(dest_path, filename_with_extension)
    image.save(dest_full_path)
    os.remove(source_full_path)


def processImageRequest(image_url, sentence):

    colorama.init(autoreset=True)

    # If no URL was providaded, returns empty string.
    if not image_url:
        return ""
    # Get first alphanumeric characters from sentence, up to a maximum of MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME.
    raw_sentence = re.sub(r'\W+', '', sentence)
    num_beginning_characters = min(MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, len(raw_sentence))
    # Generate image filename.
    filename = generateFilename("{}{}".format(IMAGE_FILENAME_PREFIX, re.sub(r'\W+', '', sentence)[:num_beginning_characters]))
    
    # Download and resize image using helper function downloadImageFromUrl()
    try:
        filename_with_extension = downloadImageFromURL(image_url, STAGING_PATH, filename)
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED + "Couldn't download image for sentence: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        return ""

    if DONT_MOVE_IMAGES:
        return ""

    # Move image to Anki medias folder.
    moveImage(filename_with_extension, IMAGE_PATH, STAGING_PATH)
    # Returns image field entry.
    return r'''<img src="{}">'''.format(filename_with_extension)


