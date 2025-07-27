# gui/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from gui.sidebar import Sidebar

# Import page modules (we'll stub these first)
from gui.pages.dashboard import DashboardPage
from gui.pages.transactions import TransactionsPage
from gui.pages.upload import UploadPage
from gui.pages.budget import BudgetPage
from gui.pages.analytics import AnalyticsPage
from gui.pages.settings import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BudgetVisualizer")
        self.setMinimumSize(1000, 700)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigate.connect(self.change_view)

        # Pages
        self.pages = QStackedWidget()
        self.page_map = {
            "dashboard": DashboardPage(),
            "transactions": TransactionsPage(),
            "upload": UploadPage(),
            "budget": BudgetPage(),
            "analytics": AnalyticsPage(),
            "settings": SettingsPage()
        }
        for page in self.page_map.values():
            self.pages.addWidget(page)

        # Layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.pages)

        self.setCentralWidget(container)
        self.change_view("dashboard")

    def change_view(self, page_name):
        page = self.page_map.get(page_name)
        if page:
            self.sidebar.set_active(page_name)
            self.pages.setCurrentWidget(page)
