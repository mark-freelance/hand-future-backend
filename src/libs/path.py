import os.path

LIBS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.dirname(LIBS_DIR)
PROJECT_DIR = os.path.dirname(SRC_DIR)

ENV_PATH = os.path.join(PROJECT_DIR, '.env')


def ensure_dir_exist(dir_path: str):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path


LOGS_DIR = ensure_dir_exist(os.path.join(PROJECT_DIR, "logs"))
DATA_DIR = ensure_dir_exist(os.path.join(PROJECT_DIR, "data"))
UPLOADED_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "uploaded"))
UPLOADED_THUMB_DATA_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "uploaded_thumb"))
AVATAR_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "avatar"))
CACHE_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "cache"))
CONFIG_DIR = ensure_dir_exist(os.path.join(DATA_DIR, "config"))

GRAPH_PATH = os.path.join(DATA_DIR, 'graph.json')
GRAPH_BAK_PATH = os.path.join(DATA_DIR, 'graph.bak.json')
