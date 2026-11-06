from PySide6.QtWebEngineCore import QWebEngineProfile
from ..config import app_data_dir, APP_NAME

class ProfileManager:
    def __init__(self):
        self.normal = QWebEngineProfile(APP_NAME)
        self.normal.setPersistentStoragePath(str(app_data_dir() / "webengine"))
        self.normal.setCachePath(str(app_data_dir() / "cache"))
        self.normal.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        self.private_profiles = []

    def create_private(self):
        profile = QWebEngineProfile()
        self.private_profiles.append(profile)
        return profile
