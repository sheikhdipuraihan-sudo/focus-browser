from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QToolButton, QMessageBox, QFileDialog, QInputDialog
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest
from PySide6.QtWebEngineWidgets import QWebEngineView
from ..config import HOME_URL, SEARCH_URL, default_download_dir
from ..data.database import Database
from .tab_bar import TabBar

class MainWindow(QMainWindow):
    def __init__(self, profiles, db):
        super().__init__(); self.profiles, self.db = profiles, db; self.setWindowTitle("SkyBrowse"); self.resize(1280, 820)
        root = QWidget(); self.setCentralWidget(root); outer = QVBoxLayout(root); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)
        nav = QHBoxLayout(); nav.setContentsMargins(8,7,8,7); nav.setSpacing(5)
        for text, slot in [("‹", self.go_back), ("›", self.go_forward), ("↻", self.reload_page), ("⌂", lambda: self.navigate(HOME_URL))]:
            b=QToolButton(); b.setText(text); b.setFixedSize(34,32); b.clicked.connect(slot); nav.addWidget(b)
        self.address = QLineEdit(); self.address.setPlaceholderText("Search or enter web address"); self.address.returnPressed.connect(lambda: self.navigate(self.address.text())); nav.addWidget(self.address, 1)
        star=QToolButton(); star.setText("☆"); star.setToolTip("Bookmark this page"); star.clicked.connect(self.toggle_bookmark); nav.addWidget(star)
        menu=QToolButton(); menu.setText("⋮"); menu.setPopupMode(QToolButton.InstantPopup); nav.addWidget(menu)
        m=menu.menu() or __import__('PySide6.QtWidgets', fromlist=['QMenu']).QMenu(menu); menu.setMenu(m)
        self.add_action(m,"New Tab", self.new_tab, "Ctrl+T"); self.add_action(m,"New Private Tab", self.private_tab, "Ctrl+Shift+N"); m.addSeparator(); self.add_action(m,"Find in Page", self.find_in_page, "Ctrl+F"); self.add_action(m,"Print to PDF", self.print_pdf); self.add_action(m,"View Source", self.view_source); self.add_action(m,"Downloads Folder", self.open_downloads); self.add_action(m,"History", self.show_history); self.add_action(m,"Bookmarks", self.show_bookmarks); m.addSeparator(); self.add_action(m,"Quit", self.close, "Ctrl+Q")
        outer.addLayout(nav); self.tabs=TabBar(profiles.normal, self); self.tabs.currentChanged.connect(self.sync_address); outer.addWidget(self.tabs); self.tabs.add_browser_tab(QUrl(HOME_URL))
        profiles.normal.downloadRequested.connect(self.handle_download)
        self.setStyleSheet("QMainWindow{background:#202124} QLineEdit{background:#303134;border:1px solid #5f6368;border-radius:17px;padding:7px 14px;color:#f1f3f4;font-size:14px} QToolButton{color:#e8eaed;background:transparent;border:0;border-radius:16px;font-size:18px} QToolButton:hover{background:#3c4043} QTabWidget::pane{border:0} QTabBar::tab{background:#292a2d;color:#bdc1c6;padding:10px 22px;border:0} QTabBar::tab:selected{background:#3c4043;color:white} #newTabTitle{color:#e8eaed}")

    def add_action(self, menu, label, slot, shortcut=None):
        a=QAction(label,self); a.triggered.connect(slot); (a.setShortcut(shortcut) if shortcut else None); menu.addAction(a); return a
    def current(self): return self.tabs.currentWidget()
    def navigate(self, text):
        text=text.strip(); url=QUrl.fromUserInput(text) if (" " not in text and ("." in text or text.startswith(("http://","https://")))) else QUrl(SEARCH_URL.format(query=QUrl.toPercentEncoding(text).data().decode()))
        self.current().setUrl(url)
    def sync_address(self, *_):
        v=self.current()
        if v: v.urlChanged.connect(lambda u: self.address.setText(u.toString())); self.address.setText(v.url().toString())
    def go_back(self): self.current().back()
    def go_forward(self): self.current().forward()
    def reload_page(self): self.current().reload()
    def new_tab(self): self.tabs.add_browser_tab(QUrl(HOME_URL))
    def private_tab(self): self.tabs.add_browser_tab(QUrl(HOME_URL), private=True)
    def toggle_bookmark(self):
        v=self.current(); url=v.url().toString();
        if self.db.is_bookmarked(url): self.db.remove_bookmark(url); QMessageBox.information(self,"Bookmark removed",url)
        else: self.db.add_bookmark(url,v.title()); QMessageBox.information(self,"Bookmark saved",v.title() or url)
    def find_in_page(self):
        text,ok=QInputDialog.getText(self,"Find in page","Text:");
        if ok: self.current().findText(text)
    def print_pdf(self):
        path,_=QFileDialog.getSaveFileName(self,"Save page as PDF",str(default_download_dir()/"page.pdf"),"PDF files (*.pdf)");
        if path: self.current().page().printToPdf(path)
    def view_source(self): self.current().setUrl(QUrl("view-source:"+self.current().url().toString()))
    def open_downloads(self): __import__('os').startfile(str(default_download_dir())) if hasattr(__import__('os'),'startfile') else None
    def show_history(self): QMessageBox.information(self,"History","\n".join(f"{t or u}\n{u}" for u,t,_ in self.db.list_history()) or "No history yet.")
    def show_bookmarks(self): QMessageBox.information(self,"Bookmarks","\n".join(f"{t or u}\n{u}" for u,t in self.db.list_bookmarks()) or "No bookmarks yet.")
    def handle_download(self, item: QWebEngineDownloadRequest):
        item.setDownloadDirectory(str(default_download_dir())); item.accept()
        item.finished.connect(lambda: QMessageBox.information(self,"Download complete",item.downloadFileName()))
