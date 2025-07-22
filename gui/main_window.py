# gui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel,
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QComboBox, QHBoxLayout,
)
from collections import defaultdict
from datetime import datetime

from core.parser import parse_transaction_file
from core.storage import save_transactions, get_all_transactions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BudgetVisualizer (Offline Mode)")
        self.setMinimumSize(900, 600)

        self.tabs = QTabWidget()
        self.upload_tab = QWidget()
        self.viewer_tab = QWidget()

        self.setup_upload_tab()
        self.setup_viewer_tab()

        self.tabs.addTab(self.upload_tab, "Upload")
        self.tabs.addTab(self.viewer_tab, "Transactions")

        self.setCentralWidget(self.tabs)

    def setup_upload_tab(self):
        self.label = QLabel("No file selected.")
        self.upload_btn = QPushButton("Upload UPI Excel or CSV File")
        self.upload_btn.clicked.connect(self.select_file)

        layout = QVBoxLayout()
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.label)
        self.upload_tab.setLayout(layout)

    def setup_viewer_tab(self):
        self.table = QTableWidget()

        # Dropdowns
        self.month_filter = QComboBox()
        self.category_filter = QComboBox()
        self.apply_filter_btn = QPushButton("Apply Filters")
        self.apply_filter_btn.clicked.connect(self.load_transactions)

        # Layout
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Month:"))
        filter_layout.addWidget(self.month_filter)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        filter_layout.addWidget(self.apply_filter_btn)

        layout = QVBoxLayout()
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        self.viewer_tab.setLayout(layout)

        self.refresh_filters()
        self.load_transactions()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select UPI Report File",
            "",
            "Excel or CSV Files (*.xlsx *.xls *.csv)"
        )
        if file_path:
            self.label.setText(f"Selected: {file_path}")
            transactions = parse_transaction_file(file_path)

            if transactions:
                save_transactions(transactions)
                QMessageBox.information(self, "Success", f"Saved {len(transactions)} transactions.")
                self.load_transactions()
            else:
                QMessageBox.warning(self, "No Data", "No transactions parsed from file.")

    def load_transactions(self):
        all_tx = get_all_transactions()
        selected_month = self.month_filter.currentText()
        selected_category = self.category_filter.currentText()

        filtered = []
        for tx in all_tx:
            try:
                dt = datetime.fromisoformat(tx["datetime"])
                tx_month = dt.strftime("%Y-%m")
                if selected_month != "All" and tx_month != selected_month:
                    continue
                if selected_category != "All" and tx.get("category") != selected_category:
                    continue
                filtered.append(tx)
            except:
                continue

        headers = ["datetime", "account", "amount", "description", "category"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(filtered))

        for row_idx, tx in enumerate(filtered):
            for col_idx, field in enumerate(headers):
                item = QTableWidgetItem(str(tx.get(field, "")))
                self.table.setItem(row_idx, col_idx, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def refresh_filters(self):
        transactions = get_all_transactions()
        months = set()
        categories = set()

        for tx in transactions:
            try:
                dt = datetime.fromisoformat(tx["datetime"])
                months.add(dt.strftime("%Y-%m"))
            except:
                continue
            categories.add(tx.get("category", "Uncategorized"))

        self.month_filter.clear()
        self.month_filter.addItem("All")
        self.month_filter.addItems(sorted(months))

        self.category_filter.clear()
        self.category_filter.addItem("All")
        self.category_filter.addItems(sorted(categories))

