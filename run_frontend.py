import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont
import os
from file_handler import upload_file

class AudioRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder")
        self.setMinimumSize(600, 400)

        # Set modern dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Top bar layout for settings and menu
        top_bar = QHBoxLayout()

        # Settings button (top-left, gear icon)
        settings_button = QPushButton()
        settings_button.setFixedSize(50, 50)
        settings_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "gear.png")))
        settings_button.setIconSize(QSize(30, 30))
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
        """)
        settings_button.clicked.connect(self.open_settings)
        top_bar.addWidget(settings_button)

        # Spacer to push menu to the right
        top_bar.addStretch()

        # Menu button (top-right, hamburger icon)
        menu_button = QPushButton()
        menu_button.setObjectName("MenuButton")  # For menu positioning
        menu_button.setFixedSize(50, 50)
        menu_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "hamburger.png")))
        menu_button.setIconSize(QSize(30, 30))
        menu_button.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
        """)
        menu_button.clicked.connect(self.show_menu)
        top_bar.addWidget(menu_button)

        main_layout.addLayout(top_bar)

        # Centered microphone button
        mic_button = QPushButton()
        mic_button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "microphone.png")))
        mic_button.setIconSize(QSize(120, 120))
        mic_button.setFixedSize(200, 200)
        mic_button.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                border: 3px solid #b4befe;
                border-radius: 100px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #b4befe;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #74c7ec;
                transform: scale(0.95);
            }
        """)
        mic_button.clicked.connect(self.toggle_recording)

        # Center the microphone button
        main_layout.addStretch()
        mic_button_layout = QHBoxLayout()
        mic_button_layout.addStretch()
        mic_button_layout.addWidget(mic_button)
        mic_button_layout.addStretch()
        main_layout.addLayout(mic_button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.is_recording = False

    def open_settings(self):
        QMessageBox.information(self, "Instellingen", "Instellingen worden hier geopend.")

    def show_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #313244;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #45475a;
            }
        """)
        menu.addAction("Nieuw", lambda: print("Nieuw geselecteerd"))
        menu.addAction("Bestand uploaden", self.handle_upload)
        menu.addAction("Opslaan", lambda: print("Opslaan geselecteerd"))
        menu.addAction("Afsluiten", self.close)
        menu.exec(self.mapToGlobal(self.findChild(QPushButton, "MenuButton").pos()))

    def handle_upload(self):
        file_path = upload_file(self)
        if file_path:
            QMessageBox.information(self, "Upload", f"Bestand geselecteerd: {file_path}")
        else:
            QMessageBox.warning(self, "Upload", "Geen bestand geselecteerd.")

    def toggle_recording(self):
        self.is_recording = not self.is_recording
        status = "Opname gestart" if self.is_recording else "Opname gestopt"
        QMessageBox.information(self, "Opname", status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    window = AudioRecorderApp()
    window.show()
    sys.exit(app.exec())