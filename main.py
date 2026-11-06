import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtWebEngineCore import QtWebEngineQuick
from browser.config import APP_NAME, ORG_NAME, app_data_dir
from browser.core.profile_manager import ProfileManager
from browser.data.database import Database
from browser.ui.main_window import MainWindow

if __name__ == "__main__":
    QCoreApplication.setOrganizationName(ORG_NAME); QCoreApplication.setApplicationName(APP_NAME)
    app=QApplication(sys.argv); app.setApplicationDisplayName(APP_NAME)
    profiles=ProfileManager(); db=Database(app_data_dir()/"browser.sqlite")
    window=MainWindow(profiles,db); window.show(); sys.exit(app.exec())
