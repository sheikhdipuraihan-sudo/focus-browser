from PySide6.QtCore import Signal, QUrl
from PySide6.QtWidgets import QTabWidget
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWebEngineView):
    new_tab_requested = Signal(QUrl)
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setPage(QWebEnginePage(profile, self))

    def createWindow(self, _type):
        tab = BrowserTab(self.page().profile())
        tab.urlChanged.connect(self.new_tab_requested)
        self.new_tab_requested.emit(QUrl("about:blank"))
        return tab

class TabBar(QTabWidget):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_browser_tab(self, url: QUrl, private=False):
        profile = self.profile
        view = BrowserTab(profile, self)
        view.new_tab_requested.connect(lambda u: self.add_browser_tab(u))
        index = self.addTab(view, "New Tab")
        self.setCurrentIndex(index)
        view.titleChanged.connect(lambda title, v=view: self.setTabText(self.indexOf(v), (title or "New Tab")[:24]))
        view.iconChanged.connect(lambda icon, v=view: self.setTabIcon(self.indexOf(v), icon))
        view.setUrl(url)
        return view

    def close_tab(self, index):
        if self.count() == 1:
            self.add_browser_tab(QUrl("about:blank"))
        widget = self.widget(index)
        self.removeTab(index)
        widget.deleteLater()
