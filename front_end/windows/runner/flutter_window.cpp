#include "flutter_window.h"

#include <optional>
#include <string>
#include <flutter/method_channel.h>
#include <flutter/standard_method_codec.h>
#include <iostream>

#include "flutter/generated_plugin_registrant.h"

FlutterWindow::FlutterWindow(const flutter::DartProject& project)
    : project_(project), isCtrlPressed_(false), isShiftPressed_(false) {}

FlutterWindow::~FlutterWindow() {}

bool FlutterWindow::OnCreate() {
  if (!Win32Window::OnCreate()) {
    return false;
  }

  RECT frame = GetClientArea();
  flutter_controller_ = std::make_unique<flutter::FlutterViewController>(
      frame.right - frame.left, frame.bottom - frame.top, project_);
  if (!flutter_controller_->engine() || !flutter_controller_->view()) {
    return false;
  }
  RegisterPlugins(flutter_controller_->engine());
  SetChildContent(flutter_controller_->view()->GetNativeWindow());

  input_channel_ = std::make_shared<flutter::MethodChannel<flutter::EncodableValue>>(
      flutter_controller_->engine()->messenger(), "input.channel",
      &flutter::StandardMethodCodec::GetInstance());
  focus_channel_ = std::make_shared<flutter::MethodChannel<flutter::EncodableValue>>(
      flutter_controller_->engine()->messenger(), "focus.channel",
      &flutter::StandardMethodCodec::GetInstance());
  focus_channel_->SetMethodCallHandler(
      [this](const flutter::MethodCall<flutter::EncodableValue>& call,
             std::unique_ptr<flutter::MethodResult<flutter::EncodableValue>> result) {
        if (call.method_name() == "focus") {
          HWND hwnd = GetHandle();
          SetForegroundWindow(hwnd);
          SetFocus(hwnd);
          std::wcout << L"Focus requested via platform channel\n";
          result->Success();
        } else {
          result->NotImplemented();
        }
      });

  flutter_controller_->engine()->SetNextFrameCallback([&]() { this->Show(); });
  flutter_controller_->ForceRedraw();
  return true;
}

void FlutterWindow::OnDestroy() {
  if (flutter_controller_) flutter_controller_ = nullptr;
  input_channel_ = nullptr;
  focus_channel_ = nullptr;
  Win32Window::OnDestroy();
}

LRESULT
FlutterWindow::MessageHandler(HWND hwnd, UINT const message,
                              WPARAM const wparam,
                              LPARAM const lparam) noexcept {
  if (flutter_controller_) {
    std::optional<LRESULT> result =
        flutter_controller_->HandleTopLevelWindowProc(hwnd, message, wparam, lparam);
    if (result) return *result;
  }

  switch (message) {
    case WM_FONTCHANGE:
      flutter_controller_->engine()->ReloadSystemFonts();
      break;
    case WM_CHAR: {
      wchar_t character = static_cast<wchar_t>(wparam);
      if (character == 8 || (GetAsyncKeyState(VK_CONTROL) & 0x8000) || character == 13) return 0;
      std::wcout << L"Received WM_CHAR: " << character << std::endl;
      std::wstring char_str(&character, 1);
      std::string utf8_char;
      int size = WideCharToMultiByte(CP_UTF8, 0, char_str.c_str(), 1, nullptr, 0, nullptr, nullptr);
      utf8_char.resize(size);
      WideCharToMultiByte(CP_UTF8, 0, char_str.c_str(), 1, utf8_char.data(), size, nullptr, nullptr);
      if (!utf8_char.empty() && input_channel_) {
        input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>(utf8_char));
      }
      return 0;
    }
    case WM_KEYDOWN: {
      bool isCtrlPressed = GetAsyncKeyState(VK_CONTROL) & 0x8000;
      bool isShiftPressed = GetAsyncKeyState(VK_SHIFT) & 0x8000;
      if (wparam == VK_CONTROL) isCtrlPressed_ = true;
      if (wparam == VK_SHIFT) isShiftPressed_ = true;
      if (wparam == VK_BACK) {
        if (isCtrlPressed) {
          std::wcout << L"Received Ctrl+Backspace\n";
          if (input_channel_) {
            input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>("CTRL_BACKSPACE"));
          }
        } else {
          std::wcout << L"Received WM_KEYDOWN: VK_BACK\n";
          if (input_channel_) {
            input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>("BACKSPACE"));
          }
        }
        return 0;
      }
      if (wparam == VK_RETURN) {
        if (isShiftPressed) {
          std::wcout << L"Received Shift+Enter\n";
          if (input_channel_) {
            input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>("SHIFT_ENTER"));
          }
        } else {
          std::wcout << L"Received Enter\n";
          if (input_channel_) {
            input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>("ENTER"));
          }
        }
        return 0;
      }
      if (wparam == 0x41 && isCtrlPressed) { // 0x41 is 'A'
        std::wcout << L"Received Ctrl+A\n";
        if (input_channel_) {
          input_channel_->InvokeMethod("input", std::make_unique<flutter::EncodableValue>("SELECT_ALL"));
        }
        return 0;
      }
      break;
    }
    case WM_KEYUP: {
      if (wparam == VK_CONTROL) isCtrlPressed_ = false;
      if (wparam == VK_SHIFT) isShiftPressed_ = false;
      break;
    }
    case WM_SETFOCUS: {
      std::wcout << L"Received WM_SETFOCUS\n";
      if (input_channel_) {
        input_channel_->InvokeMethod("focus", std::make_unique<flutter::EncodableValue>(true));
      }
      break;
    }
  }
  return Win32Window::MessageHandler(hwnd, message, wparam, lparam);
}