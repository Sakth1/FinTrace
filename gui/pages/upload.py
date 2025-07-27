# gui/pages/upload.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from core.parser import parse_transaction_file
from core.storage import save_transactions


class UploadPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload Transactions")

        layout = QVBoxLayout()

        title = QLabel("📤 Upload UPI Report")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.upload_btn = QPushButton("Select UPI Excel or CSV File")
        self.upload_btn.clicked.connect(self.select_file)

        self.status_label = QLabel("No file uploaded yet.")
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select UPI Report File",
            "",
            "Excel or CSV Files (*.xlsx *.xls *.csv)"
        )
        if file_path:
            self.status_label.setText(f"Selected: {file_path}")
            transactions = parse_transaction_file(file_path)

            if transactions:
                save_transactions(transactions)
                QMessageBox.information(self, "Success", f"Imported {len(transactions)} transactions.")
            else:
                QMessageBox.warning(self, "No Data", "No transactions parsed from the file.")
