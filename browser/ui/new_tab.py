from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PySide6.QtGui import QFont

class NewTabPage(QWidget):
    def __init__(self, navigate, parent=None):
        super().__init__(parent); self.navigate = navigate
        layout = QVBoxLayout(self); layout.setContentsMargins(80, 120, 80, 80); layout.setSpacing(18)
        title = QLabel("SkyBrowse"); title.setFont(QFont("Segoe UI", 34, QFont.Weight.DemiBold)); title.setObjectName("newTabTitle")
        self.entry = QLineEdit(); self.entry.setPlaceholderText("Search the web or enter an address"); self.entry.returnPressed.connect(lambda: self.navigate(self.entry.text()))
        layout.addWidget(title); layout.addWidget(self.entry); layout.addStretch()
