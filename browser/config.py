from pathlib import Path
from PySide6.QtCore import QStandardPaths

APP_NAME = "SkyBrowse"
ORG_NAME = "SkyBrowse"
HOME_URL = "https://www.google.com/"
SEARCH_URL = "https://www.google.com/search?q={query}"


def app_data_dir() -> Path:
    root = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
    root.mkdir(parents=True, exist_ok=True)
    return root


def default_download_dir() -> Path:
    root = Path(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)) / APP_NAME
    root.mkdir(parents=True, exist_ok=True)
    return root
