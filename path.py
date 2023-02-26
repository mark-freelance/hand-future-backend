import os.path

PROJECT_DIR = os.path.dirname(__file__)


def ensure_dir_exist(dir_path: str):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


LOGS_DIR = ensure_dir_exist(os.path.join(PROJECT_DIR, "logs"))
DATA_DIR = ensure_dir_exist(os.path.join(PROJECT_DIR, "data"))
UPLOADED_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "uploaded"))
UPLOADED_THUMB_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "uploaded_thumb"))
AVATAR_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "avatar"))
CACHE_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "cache"))
CONFIG_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "config"))

GRAPH_DATA_PATH = os.path.join(DATA_DIR, 'graph.json')
GRAPH_DATA_BAK_PATH = os.path.join(DATA_DIR, 'graph.bak.json')
