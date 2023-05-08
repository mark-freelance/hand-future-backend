import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.libs.path import UPLOADED_DIR

os.chdir(UPLOADED_DIR)
for filename in os.listdir('.'):
    # filename_new = unquote(filename)
    filename_new = filename[:32] + ".png"
    print({"old": filename, "new": filename_new})
    os.rename(filename, filename_new)
