#ifndef RUNNER_FLUTTER_WINDOW_H_
#define RUNNER_FLUTTER_WINDOW_H_

#include <flutter/dart_project.h>
#include <flutter/flutter_view_controller.h>
#include <flutter/method_channel.h>
#include <flutter/standard_method_codec.h>

#include <memory>

#include "win32_window.h"

// A window that does nothing but host a Flutter view.
class FlutterWindow : public Win32Window {
 public:
  explicit FlutterWindow(const flutter::DartProject& project);
  virtual ~FlutterWindow();
  flutter::FlutterViewController* controller() const { return flutter_controller_.get(); }

 protected:
  bool OnCreate() override;
  void OnDestroy() override;
  LRESULT MessageHandler(HWND window, UINT const message, WPARAM const wparam,
                         LPARAM const lparam) noexcept override;

 private:
  flutter::DartProject project_;
  std::unique_ptr<flutter::FlutterViewController> flutter_controller_;
  std::shared_ptr<flutter::MethodChannel<flutter::EncodableValue>> input_channel_;
  std::shared_ptr<flutter::MethodChannel<flutter::EncodableValue>> focus_channel_;
  bool isCtrlPressed_ = false;
  bool isShiftPressed_ = false; // Member voor Shift-status
};

#endif  // RUNNER_FLUTTER_WINDOW_H_