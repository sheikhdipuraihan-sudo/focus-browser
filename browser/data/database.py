import sqlite3
from pathlib import Path
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, url TEXT NOT NULL, title TEXT, visited_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS bookmarks (id INTEGER PRIMARY KEY, url TEXT UNIQUE NOT NULL, title TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
"""

class Database:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db: db.executescript(SCHEMA)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        try:
            yield db
            db.commit()
        finally:
            db.close()

    def add_history(self, url: str, title: str):
        if url and not url.startswith("sky:"):
            with self.connect() as db: db.execute("INSERT INTO history(url,title) VALUES (?,?)", (url, title))

    def list_history(self, limit=200):
        with self.connect() as db: return db.execute("SELECT url,title,visited_at FROM history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()

    def add_bookmark(self, url: str, title: str):
        with self.connect() as db: db.execute("INSERT OR REPLACE INTO bookmarks(url,title) VALUES (?,?)", (url, title))

    def remove_bookmark(self, url: str):
        with self.connect() as db: db.execute("DELETE FROM bookmarks WHERE url=?", (url,))

    def is_bookmarked(self, url: str):
        with self.connect() as db: return db.execute("SELECT 1 FROM bookmarks WHERE url=?", (url,)).fetchone() is not None

    def list_bookmarks(self):
        with self.connect() as db: return db.execute("SELECT url,title FROM bookmarks ORDER BY title COLLATE NOCASE").fetchall()

    def clear_history(self):
        with self.connect() as db: db.execute("DELETE FROM history")
