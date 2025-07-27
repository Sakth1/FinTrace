# gui/pages/dashboard.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("📊 Dashboard Page"))
        self.setLayout(layout)
