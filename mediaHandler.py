import requests
import shutil
import re
import os
import colorama
from PIL import Image
from math import floor
from random import choice
from google.cloud import texttospeech_v1 as tts
from definitions import MAXIMUM_BEGINNING_CHARACTERS_IMAGE_FILENAME, STAGING_PATH, ANKI_MEDIA_PATH, \
    MEDIA_FILENAME_PREFIX, IMAGE_HEIGHT, DONT_MOVE_MEDIA, GOOGLE_TTS_CREDENTIALS_FULL_PATH
from utilities import generateFilename



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

def processTtsRequest(repl_line, sentence, dest_filename):

    # TODO: Make this more general, not specific to French and current valid Wavenet voices.

    # Set credentials environment variable and initialize text to speech client.
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_TTS_CREDENTIALS_FULL_PATH
    client = tts.TextToSpeechClient()

    # Use "wa" as shorthand for "fr-fr-wavenet-a" etc.
    voice_name = re.sub(r"^w([a-e])\s*$", r"fr-fr-wavenet-\1", repl_line, count=1, flags=re.IGNORECASE)

    # Use "w" or "w." as shorthand for a random fr-fr wavenet voice.
    voice_name = re.sub(r"^w\.?\s*$", r"fr-fr-wavenet-{}".format(choice(["a", "b", "c", "d", "e"])), voice_name, count=1, flags=re.IGNORECASE)

    # Use "sa" as shorthand for "fr-fr-studio-a" etc. Only "a" and "d" are currently available.
    voice_name = re.sub(r"^s([ad])\s*$", r"fr-fr-studio-\1", voice_name, count=1, flags=re.IGNORECASE)

    # Use "s" or "s." as shorthand for a random fr-fr studio voice.
    voice_name = re.sub(r"^s\.?\s*$", r"fr-fr-studio-{}".format(choice(["a", "d"])), voice_name, count=1, flags=re.IGNORECASE)

    # Specify voice and configuration parameters for Google TTS.
    voice = tts.VoiceSelectionParams(
        language_code='fr-FR',
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )

    # Synthetize sentence recording.
    response = client.synthesize_speech(
        request={"input": tts.SynthesisInput(text=sentence), "voice": voice, "audio_config": audio_config}
    )

    # Save audio file in the staging directory.
    with open(r"{}{}.mp3".format(STAGING_PATH, dest_filename), "wb") as out:
        out.write(response.audio_content)

    # Return audio file name.
    return "{}.mp3".format(dest_filename)


def processAudioRequest(audio_file, dest_filename, sentence):

    if not audio_file:
        return ""

    repl_line, match = re.subn("^tts:\s*", "", audio_file, count=1, flags=re.IGNORECASE)
    if match:
        source_filename_with_extension = processTtsRequest(repl_line, sentence, dest_filename)

    else:
        source_filename_with_extension = audio_file # TODO: Improve variable names.

    extension = re.search(r"\.([a-z0-9]*)$", source_filename_with_extension).group(1)

    # Get audio filename with extension.
    dest_filename_with_extension = r"{}.{}".format(dest_filename, extension)

    if not DONT_MOVE_MEDIA:
        # Move audio to Anki medias folder.
        shutil.move(r"{}{}".format(STAGING_PATH, source_filename_with_extension), r"{}{}".format(ANKI_MEDIA_PATH, dest_filename_with_extension)) # TODO: Allow audio source path to be specified as command line option.

    return r"[sound:{}]".format(dest_filename_with_extension)


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
    except Exception as e:
        print(colorama.Fore.RED + "Error processing image request: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        image_field = ""
    try:
        audio_field = processAudioRequest(audio_file, filename, sentence)
    except Exception as e:
        print(colorama.Fore.RED + "Error processing audio request: \"{}\"\n{}".format(sentence, repr(e)), end="\n\n")
        audio_field = ""

    return image_field, audio_field




