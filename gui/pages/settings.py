# gui/pages/settings.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QCheckBox, QMessageBox
)
from core.storage import load_settings, save_settings
from pathlib import Path


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        layout = QVBoxLayout()

        title = QLabel("⚙️ Application Settings")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Offline Mode Toggle
        self.offline_checkbox = QCheckBox("Enable Offline Mode (No Gmail access)")
        self.offline_checkbox.stateChanged.connect(self.toggle_offline)

        layout.addWidget(self.offline_checkbox)

        # Data folder info
        layout.addWidget(QLabel(f"Local Data Path: {Path('data/db.json').resolve()}"))

        self.setLayout(layout)
        self.load_user_settings()

    def load_user_settings(self):
        settings = load_settings()
        # Assuming settings is a list of Document objects and offline_mode is an attribute
        offline_mode = True
        if settings and hasattr(settings[0], "offline_mode"):
            offline_mode = getattr(settings[0], "offline_mode", True)
        self.offline_checkbox.setChecked(offline_mode)

    def toggle_offline(self, state):
        offline = bool(state)
        save_settings({"offline_mode": offline})
        QMessageBox.information(self, "Settings Updated", f"Offline Mode set to: {offline}")
