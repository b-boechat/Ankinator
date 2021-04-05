import urllib.request
from urllib.error import HTTPError
import re
from PIL import Image
from math import floor
from definitions import MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, STAGING_PATH, IMAGE_PATH, IMAGE_FILENAME_PREFIX, IMAGE_HEIGHT, DONT_MOVE_IMAGES
from utilities import generateFilename
import os
import colorama


def downloadImageFromURL(url, path, filename):
    # Install opener to avoid Error 403. See: https://stackoverflow.com/questions/34692009/download-image-from-url-using-python-urllib-but-receiving-http-error-403-forbid
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent',r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    # Get image extension from URL.
    extension = re.search(r"\.([a-z]*)$", url).group(1)
    # Get filename with extension.
    filename_with_extension = r"{}.{}".format(filename, extension)
    # Generate full staging path.
    full_path = r"{}{}".format(path, filename_with_extension)
    # Download image from URL, saving on staging path.

    urllib.request.urlretrieve(url, full_path)

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

    colorama.init()

    # If no URL was providaded, returns empty string.
    if not image_url:
        return ""
    # Get first alphanumeric characters from sentence, up to a maximum of MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME.
    raw_sentence = re.sub(r'\W+', '', sentence)
    num_beginning_characters = min(MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, len(raw_sentence))
    # Generate image filename.
    filename = generateFilename("{}{}".format(IMAGE_FILENAME_PREFIX, re.sub(r'\W+', '', sentence)[:num_beginning_characters]))
    try:
        # Download and resize image using helper function downloadImageFromUrl()
        filename_with_extension = downloadImageFromURL(image_url, STAGING_PATH, filename)
    except HTTPError as e:
        print(colorama.Fore.RED + "Couldn't download image for sentence: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        return ""
    except Exception as e:
        print(colorama.Fore.RED + "Couldn't download image for sentence: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        return ""

    if DONT_MOVE_IMAGES:
        return ""

    # Move image to Anki medias folder.
    moveImage(filename_with_extension, IMAGE_PATH, STAGING_PATH)
    # Returns image field entry.
    return r'''<img src="{}">'''.format(filename_with_extension)


