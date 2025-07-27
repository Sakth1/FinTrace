# gui/components/card.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class SummaryCard(QFrame):
    def __init__(self, title, value, color="black"):
        super().__init__()
        self.setObjectName("card")
        self.setFrameShape(QFrame.Box)
        self.setStyleSheet("""
            QFrame#card {
                background-color: #f4f4f4;
                border-radius: 12px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")

        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"font-size: 20px; color: {color}; font-weight: 600;")

        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
