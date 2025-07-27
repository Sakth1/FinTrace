# gui/sidebar.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Signal


class Sidebar(QWidget):
    navigate = Signal(str)  # Emits: "dashboard", "transactions", etc.

    def __init__(self):
        super().__init__()
        self.setFixedWidth(180)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.buttons = {}
        for name, label in [
            ("dashboard", "Home"),
            ("transactions", "Transactions"),
            ("upload", "Upload Data"),
            ("budget", "Budget"),
            ("analytics", "Analytics"),
            ("settings", "Settings")
        ]:
            btn = QPushButton(label)
            btn.setObjectName(name)
            btn.clicked.connect(lambda _, route=name: self.navigate.emit(route))
            layout.addWidget(btn)
            self.buttons[name] = btn

        layout.addStretch()
        self.setLayout(layout)

    def set_active(self, name):
        for key, btn in self.buttons.items():
            btn.setStyleSheet("background-color: #4CAF50;" if key == name else "")
