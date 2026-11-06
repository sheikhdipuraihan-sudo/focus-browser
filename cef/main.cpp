#include "include/cef_app.h"
#include "include/cef_browser.h"
#include "include/cef_command_line.h"
#include "include/cef_sandbox_win.h"

class FocusApp final : public CefApp, public CefBrowserProcessHandler {
 public:
  FocusApp() = default;
  CefRefPtr<CefBrowserProcessHandler> GetBrowserProcessHandler() override { return this; }
  void OnBeforeCommandLineProcessing(const CefString& process_type,
                                     CefRefPtr<CefCommandLine> command_line) override {
    if (process_type.empty()) {
      // CEF's Chrome runtime uses Chromium's chrome-layer runtime instead of Alloy.
      command_line->AppendSwitch("enable-chrome-runtime");
    }
  }
  IMPLEMENT_REFCOUNTING(FocusApp);
};

class FocusClient final : public CefClient, public CefLifeSpanHandler {
 public:
  CefRefPtr<CefLifeSpanHandler> GetLifeSpanHandler() override { return this; }
  void OnAfterCreated(CefRefPtr<CefBrowser> browser) override { browser_ = browser; }
  bool DoClose(CefRefPtr<CefBrowser>) override { return false; }
  void OnBeforeClose(CefRefPtr<CefBrowser>) override { browser_ = nullptr; }
  IMPLEMENT_REFCOUNTING(FocusClient);
 private:
  CefRefPtr<CefBrowser> browser_;
};

int APIENTRY wWinMain(HINSTANCE hInstance, HINSTANCE, wchar_t*, int) {
  CefMainArgs main_args(hInstance);
  CefRefPtr<FocusApp> app(new FocusApp());
  int exit_code = CefExecuteProcess(main_args, app, nullptr);
  if (exit_code >= 0) return exit_code;

  CefSettings settings;
  settings.no_sandbox = true;
  CefInitialize(main_args, settings, app, nullptr);

  CefWindowInfo window_info;
  window_info.SetAsPopup(nullptr, L"Focus");
  CefBrowserSettings browser_settings;
  CefRefPtr<FocusClient> client(new FocusClient());
  CefBrowserHost::CreateBrowser(window_info, client, "https://www.google.com/", browser_settings, nullptr, nullptr);
  CefRunMessageLoop();
  CefShutdown();
  return 0;
}
