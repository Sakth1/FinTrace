# gui/pages/dashboard.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QGroupBox,
    QHBoxLayout, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QColor
from gui.components.card import SummaryCard
from gui.components.chart import DonutChart
from core.storage import get_all_transactions, get_budget_for_month
from datetime import datetime


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Page title
        title = QLabel("Dashboard – Your Financial Overview")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Compute stats
        month_key = datetime.now().strftime("%Y-%m")
        income, expense = 0, 0

        for tx in get_all_transactions():
            try:
                tx_month = datetime.fromisoformat(tx["datetime"]).strftime("%Y-%m")
                if tx_month == month_key:
                    amt = float(tx["amount"])
                    if amt > 0:
                        income += amt
                    else:
                        expense += abs(amt)
            except:
                continue

        net_savings = income - expense
        budget = get_budget_for_month(month_key) or 0
        used_pct = (expense / budget) * 100 if budget > 0 else 0

        # Summary Cards Grid
        card_grid = QGridLayout()
        card_grid.setSpacing(15)
        card_grid.addWidget(SummaryCard("Monthly Income", f"₹{income:,.2f}", color="green"), 0, 0)
        card_grid.addWidget(SummaryCard("Monthly Expense", f"₹{expense:,.2f}", color="red"), 0, 1)
        card_grid.addWidget(SummaryCard("Net Savings", f"₹{net_savings:,.2f}", color="green"), 0, 2)
        card_grid.addWidget(SummaryCard("Budget Used", f"{used_pct:.0f}%", color="black"), 0, 3)
        layout.addLayout(card_grid)

        # Bottom row: Recent transactions + budget chart
        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.build_recent_transactions())

        chart_card = QGroupBox("Budget Usage")
        chart_layout = QVBoxLayout()
        chart_layout.addWidget(DonutChart(used_pct, "Used"))
        chart_card.setLayout(chart_layout)
        bottom_row.addWidget(chart_card)

        layout.addLayout(bottom_row)
        self.setLayout(layout)

    def build_recent_transactions(self):
        txns = sorted(get_all_transactions(), key=lambda x: x["datetime"], reverse=True)[:3]

        def format_amount(amount):
            amt = f"₹{abs(amount):,.2f}"
            return f"-{amt}" if amount < 0 else amt

        list_widget = QListWidget()
        for tx in txns:
            try:
                dt = datetime.fromisoformat(tx["datetime"]).strftime("%d %b, %I:%M %p")
                desc = tx["description"]
                amount = float(tx["amount"])
                display = f"{desc} | {dt} | {format_amount(amount)}"
                item = QListWidgetItem(display)
                item.setForeground(QColor("red") if amount < 0 else QColor("green"))
                list_widget.addItem(item)
            except:
                continue

        group = QGroupBox("Recent Transactions")
        vbox = QVBoxLayout()
        vbox.addWidget(list_widget)
        group.setLayout(vbox)
        return group
