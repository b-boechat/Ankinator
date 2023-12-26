from definitions import STAGING_PATH
import os
import re
from glob import glob

def cleanStagingFolder():
    file_paths = glob(STAGING_PATH + "*")
    for path in file_paths:
        if not re.search(r"\.gitignore$", path):
            os.remove(path)