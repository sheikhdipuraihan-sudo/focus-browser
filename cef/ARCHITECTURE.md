# Focus CEF Chrome-runtime track

This track targets stronger Chrome extension compatibility than Electron's supported subset. It uses the Chromium Embedded Framework with the Chrome runtime enabled, rather than the lighter Alloy runtime.

## Why CEF Chrome runtime

CEF exposes `CefRequestContext::LoadExtension` and extension handlers. The CEF documentation also distinguishes the Chrome runtime from Alloy because the Chrome runtime uses Chromium's `chrome` browser layer, where extension behavior lives. The trade-off is a native Windows C++ host, larger runtime resources, and a more involved build than Electron.

## Important boundary

This is not a promise of perfect Chrome Web Store compatibility. CEF's supported API list is version-specific and can be inspected with `chrome://extensions-support`. Full compatibility with every Chrome extension still requires maintaining Chromium/CEF patches or using Chrome itself.

## Migration stages

1. Keep the Electron Focus app as a fallback and release path.
2. Add the CEF SDK and native host on `windows-latest`.
3. Start CEF with the Chrome runtime switch and persist a browser context.
4. Implement tabs, downloads, navigation, and extension handlers in the native host.
5. Add an extension manager that loads unpacked directories and validates manifests.
6. Test representative Manifest V3 extensions against `chrome://extensions-support`.
7. Promote the CEF artifact only after the Windows smoke test launches and loads a test extension.

CEF build resources are intentionally not vendored into this repository because the SDK is a large, versioned binary distribution.
