from datetime import datetime
from uuid import uuid4
from shutil import copy2
from definitions import BACKUP_PATH, DONT_MOVE_MEDIA, DONT_UPDATE_DICTIONARY
import os
import colorama

def generateFilename(beginning):
    # Generates filename that starts with "beginning" followed by date in YYYY-MM-DD_HH-MM-SS- format, followed by a pseudo-random string.
    # File extension is not included.
    return "{}_{}___{}".format(beginning, datetime.today().isoformat(sep="_", timespec="seconds").replace(':', '-'), str(uuid4().hex)[:10])

def backupFile(file_full_path, backup_filename):
    # Creates backup of specified file.
    if os.path.exists(file_full_path):
        copy2(file_full_path, "{}{}.txt".format(BACKUP_PATH, generateFilename(backup_filename)))

def displayFlagReminders(dont_move_images_reminder=True, dont_update_dictionary_reminder=True):
    colorama.init(autoreset=True)
    if dont_move_images_reminder and DONT_MOVE_MEDIA:
        print(colorama.Fore.CYAN + "Reminder: DONT_MOVE_MEDIA is active.")
    if dont_update_dictionary_reminder and DONT_UPDATE_DICTIONARY:
        print(colorama.Fore.CYAN + "Reminder: DONT_UPDATE_DICTIONARY is active.")
