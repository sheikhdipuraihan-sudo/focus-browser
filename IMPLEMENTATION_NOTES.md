# Implementation notes

Qt WebEngine's profile API provides persistent storage, an off-the-record profile for private browsing, and a `downloadRequested` signal whose request must be explicitly accepted. Its page API provides find-in-page, print-to-PDF, view-source navigation, zoom, JavaScript execution, and DevTools page attachment.

Qt WebEngine does not expose the full Chrome extension API or Chrome Web Store runtime. SkyBrowse does not fake extension installation. Extension compatibility is intentionally documented as a future architecture decision requiring a different integration layer or a native Chromium extension bridge.

The Windows workflow uses PyInstaller plus `windeployqt`, following Qt for Python deployment guidance for collecting Qt plugins, WebEngine resources, and translations. The workflow runs on `windows-latest` and validates that the executable is present before uploading the distributable.

Sources:

- https://doc.qt.io/qt-6/qwebengineprofile.html
- https://doc.qt.io/qt-6/qwebenginepage.html
- https://doc.qt.io/qt-6/qtwebengine-features.html
- https://doc.qt.io/qtforpython-6/deployment/deployment-pyinstaller.html
