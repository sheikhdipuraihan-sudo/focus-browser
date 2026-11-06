# Focus

Focus is a lightweight Windows Chromium browser with a Chrome-inspired interface and a real extension-management path. The primary implementation uses Electron because QtWebEngine does not expose the Chrome extension runtime needed by this requirement.

## Extension support

Focus loads **unpacked Chromium extensions** through Electron's persistent `session.extensions.loadExtension` API, remembers their paths across launches, lists installed extensions, and removes them. Electron officially supports a subset of Chrome APIs including runtime, scripting, storage, tabs, webRequest, and DevTools APIs. It does not promise arbitrary Chrome Web Store compatibility or packed `.crx` installation; unsupported extension APIs fail honestly instead of being simulated.

## Current app

The Electron track includes multiple tabs, address/search navigation, back/forward/reload, downloads to the Windows Downloads folder, persistent Chromium session data, and an Extensions panel. The earlier PySide6/QtWebEngine prototype remains in the repository as a reference for the Qt implementation and data layer.

## Run on Windows

```powershell
npm install
npm start
```

## Package a Windows build

```powershell
npm run dist
```

Electron Builder produces NSIS and portable Windows packages. The old Qt workflow is retained for comparison in `.github/workflows/windows-build.yml`; the Focus release workflow should use Electron Builder for the primary artifact.

## Sources

- Electron Chrome Extension Support: https://electronjs.org/docs/latest/api/extensions
- Electron Session API: https://electronjs.org/docs/latest/api/session
- Qt WebEngine Profile API: https://doc.qt.io/qt-6/qwebengineprofile.html
