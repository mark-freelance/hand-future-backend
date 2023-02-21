import os
import sys
from urllib.parse import unquote

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from path import UPLOADED_DATA_DIR

os.chdir(UPLOADED_DATA_DIR)
for filename in os.listdir('.'):
    # filename_new = unquote(filename)
    filename_new = filename[:32] + ".png"
    print({"old": filename, "new": filename_new})
    os.rename(filename, filename_new)
