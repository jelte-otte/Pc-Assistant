#include "flutter_window.h"

#include <optional>
#include <string>

#include "flutter/generated_plugin_registrant.h"

FlutterWindow::FlutterWindow(const flutter::DartProject& project)
    : project_(project) {}

FlutterWindow::~FlutterWindow() {}

bool FlutterWindow::OnCreate() {
  if (!Win32Window::OnCreate()) {
    return false;
  }

  RECT frame = GetClientArea();

  // The size here must match the window dimensions to avoid unnecessary surface
  // creation / destruction in the startup path.
  flutter_controller_ = std::make_unique<flutter::FlutterViewController>(
      frame.right - frame.left, frame.bottom - frame.top, project_);
  // Ensure that basic setup of the controller was successful.
  if (!flutter_controller_->engine() || !flutter_controller_->view()) {
    return false;
  }
  RegisterPlugins(flutter_controller_->engine());
  SetChildContent(flutter_controller_->view()->GetNativeWindow());

  flutter_controller_->engine()->SetNextFrameCallback([&]() {
    this->Show();
  });

  // Flutter can complete the first frame before the "show window" callback is
  // registered. The following call ensures a frame is pending to ensure the
  // window is shown. It is a no-op if the first frame hasn't completed yet.
  flutter_controller_->ForceRedraw();

  return true;
}

void FlutterWindow::OnDestroy() {
  if (flutter_controller_) {
    flutter_controller_ = nullptr;
  }

  Win32Window::OnDestroy();
}

LRESULT
FlutterWindow::MessageHandler(HWND hwnd, UINT const message,
                              WPARAM const wparam,
                              LPARAM const lparam) noexcept {
  // Give Flutter, including plugins, an opportunity to handle window messages.
  if (flutter_controller_) {
    std::optional<LRESULT> result =
        flutter_controller_->HandleTopLevelWindowProc(hwnd, message, wparam,
                                                      lparam);
    if (result) {
      return *result;
    }
  }

  switch (message) {
    case WM_FONTCHANGE:
      flutter_controller_->engine()->ReloadSystemFonts();
      break;
    case WM_CHAR: {
      // Vang toetsaanslagen (tekens) op
      wchar_t character = static_cast<wchar_t>(wparam);
      std::wstring char_str(&character, 1);
      std::string utf8_char;
      // Reserveer ruimte voor UTF-8 conversie
      int size = WideCharToMultiByte(CP_UTF8, 0, char_str.c_str(), -1, nullptr, 0, nullptr, nullptr);
      utf8_char.resize(size);
      WideCharToMultiByte(CP_UTF8, 0, char_str.c_str(), -1, utf8_char.data(), size, nullptr, nullptr);
      // Stuur naar Flutter via platform channel
      flutter_controller_->engine()->messenger()->InvokeMethod(
          "input.channel", std::make_unique<flutter::EncodableValue>(utf8_char));
      return 0; // Markeer als afgehandeld
    }
    case WM_KEYDOWN: {
      // Vang speciale toetsen zoals backspace
      if (wparam == VK_BACK) {
        flutter_controller_->engine()->messenger()->InvokeMethod(
            "input.channel", std::make_unique<flutter::EncodableValue>("BACKSPACE"));
        return 0;
      }
      break;
    }
  }

  return Win32Window::MessageHandler(hwnd, message, wparam, lparam);
}