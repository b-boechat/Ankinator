from datetime import datetime
from uuid import uuid4
from shutil import copy2
from definitions import BACKUP_PATH

def generateFilename(beginning):
    # Generates filename that starts with "beginning" followed by date in YYYY-MM-DD_HH-MM-SS- format, followed by a pseudo-random string.
    # File extension is not included.
    return "{}_{}___{}".format(beginning, datetime.today().isoformat(sep="_", timespec="seconds").replace(':', '-'), str(uuid4().hex)[:10])

def backupFile(file_full_path, backup_filename):
    # Creates backup of specified file.
    copy2(file_full_path, "{}{}.txt".format(BACKUP_PATH, generateFilename(backup_filename)))