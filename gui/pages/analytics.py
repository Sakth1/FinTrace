# gui/pages/analytics.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout
)
from datetime import datetime
from collections import defaultdict
from core.storage import get_all_transactions
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analytics")
        self.main_layout = QVBoxLayout()

        title = QLabel("📊 Analytics – Spending by Category")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.main_layout.addWidget(title)

        self.month_dropdown = QComboBox()
        self.month_dropdown.currentTextChanged.connect(self.update_charts)

        self.chart_layout = QHBoxLayout()

        self.main_layout.addWidget(self.month_dropdown)
        self.main_layout.addLayout(self.chart_layout)
        self.setLayout(self.main_layout)

        self.refresh_months()

    def refresh_months(self):
        months = set()
        for tx in get_all_transactions():
            try:
                dt = datetime.fromisoformat(tx["datetime"])
                months.add(dt.strftime("%Y-%m"))
            except:
                continue
        self.month_dropdown.addItems(sorted(months))
        if months:
            self.update_charts()

    def update_charts(self):
        month = self.month_dropdown.currentText()
        txns = [tx for tx in get_all_transactions()
                if datetime.fromisoformat(tx["datetime"]).strftime("%Y-%m") == month]

        # Pie chart: Expense by category
        category_totals = defaultdict(float)
        income_total, expense_total = 0, 0

        for tx in txns:
            try:
                amt = float(tx["amount"])
                if amt < 0:
                    category_totals[tx["category"]] += abs(amt)
                    expense_total += abs(amt)
                else:
                    income_total += amt
            except:
                continue

        # Clear previous charts
        for i in reversed(range(self.chart_layout.count())):
            self.chart_layout.itemAt(i).widget().deleteLater()

        if category_totals:
            fig1 = Figure(figsize=(3.5, 3.5))
            ax1 = fig1.add_subplot(111)
            ax1.pie(
                list(category_totals.values()),
                labels=list(category_totals.keys()),
                autopct='%1.1f%%',
                startangle=90
            )
            ax1.set_title("Expenses by Category")
            canvas1 = Canvas(fig1)
            self.chart_layout.addWidget(canvas1)

        # Bar chart: Income vs Expense
        fig2 = Figure(figsize=(3.5, 3.5))
        ax2 = fig2.add_subplot(111)
        ax2.bar(["Income", "Expense"], [income_total, expense_total], color=["green", "red"])
        ax2.set_title("Income vs Expense")
        canvas2 = Canvas(fig2)
        self.chart_layout.addWidget(canvas2)
