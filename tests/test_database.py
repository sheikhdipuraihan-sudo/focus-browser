from browser.data.database import Database

def test_bookmarks_and_history(tmp_path):
    db=Database(tmp_path/"browser.sqlite")
    db.add_bookmark("https://example.com", "Example")
    assert db.is_bookmarked("https://example.com")
    db.add_history("https://example.com", "Example")
    assert db.list_history()[0][0] == "https://example.com"
    db.remove_bookmark("https://example.com")
    assert not db.is_bookmarked("https://example.com")
