from datetime import datetime
from uuid import uuid4

def generateFilename(beginning):
    # Generates filename that starts with "beginning" followed by date in YYYY-MM-DD_HH-MM-SS- format, followed by a pseudo-random string.
    # File extension is not included.
    return "{}_{}___{}".format(beginning, datetime.today().isoformat(sep="_", timespec="seconds").replace(':', '-'), str(uuid4().hex)[:10])
