# gui/pages/transactions.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from core.storage import get_all_transactions
from datetime import datetime


class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transactions")
        self.layout = QVBoxLayout()

        title = QLabel("📄 All Transactions")   
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(title)

        # Filters
        self.month_filter = QComboBox()
        self.category_filter = QComboBox()
        self.apply_filter_btn = QPushButton("Apply Filters")
        self.apply_filter_btn.clicked.connect(self.load_transactions)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Month:"))
        filter_layout.addWidget(self.month_filter)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        filter_layout.addWidget(self.apply_filter_btn)

        self.layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.refresh_filters()
        self.load_transactions()

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
                value = str(tx.get(field, ""))
                item = QTableWidgetItem(value)
                self.table.setItem(row_idx, col_idx, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
