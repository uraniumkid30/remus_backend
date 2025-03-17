from conf.env_manager import py_env
from .directories import create_neccessary_directories

if py_env.bool("CREATE_DEFAULT_DIRECTORIES", True):
    create_neccessary_directories()
else:
    LOGS_DIR = ""
    GUNICORN_DIR = ""
    THEME_DIR = ""
    TEMPLATES_DIR = ""
    REQUIREMENTS_DIR = ""
    STATIC_DIR = "/vol/web/static/"
    MEDIA_DIR = "/vol/web/media/"
    STATIC_COLLECTION_DIR = ""
