# gui/pages/budget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from core.storage import get_all_transactions, save_budget_for_month, get_all_budgets
from datetime import datetime


class BudgetPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monthly Budgets")

        layout = QVBoxLayout()
        title = QLabel("💸 Set Monthly Budgets by Category")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Form
        self.month_input = QComboBox()
        self.category_input = QComboBox()
        self.limit_input = QLineEdit()
        self.limit_input.setPlaceholderText("Enter budget limit (₹)")

        self.save_btn = QPushButton("Save Budget")
        self.save_btn.clicked.connect(self.save_budget)

        form = QHBoxLayout()
        form.addWidget(QLabel("Month:"))
        form.addWidget(self.month_input)
        form.addWidget(QLabel("Category:"))
        form.addWidget(self.category_input)
        form.addWidget(self.limit_input)
        form.addWidget(self.save_btn)

        layout.addLayout(form)

        # Budget Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_inputs()
        self.load_budgets()

    def refresh_inputs(self):
        txns = get_all_transactions()
        months = set()
        categories = set()

        for tx in txns:
            try:
                dt = datetime.fromisoformat(tx["datetime"])
                months.add(dt.strftime("%Y-%m"))
                categories.add(tx.get("category", "Uncategorized"))
            except:
                continue

        self.month_input.clear()
        self.month_input.addItems(sorted(months))

        self.category_input.clear()
        self.category_input.addItems(sorted(categories))

    def save_budget(self):
        month = self.month_input.currentText()
        category = self.category_input.currentText()
        try:
            limit = float(self.limit_input.text().replace(",", ""))
            save_budget_for_month(month, category, limit)
            QMessageBox.information(self, "Saved", f"Budget saved for {category} in {month}.")
            self.load_budgets()
        except ValueError:
            QMessageBox.warning(self, "Invalid", "Please enter a valid numeric budget limit.")

    def load_budgets(self):
        budgets = get_all_budgets()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Month", "Category", "Limit (₹)"])
        self.table.setRowCount(len(budgets))

        for i, b in enumerate(budgets):
            self.table.setItem(i, 0, QTableWidgetItem(b["month"]))
            self.table.setItem(i, 1, QTableWidgetItem(b["category"]))
            self.table.setItem(i, 2, QTableWidgetItem(f"₹{b['limit']:,.2f}"))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
