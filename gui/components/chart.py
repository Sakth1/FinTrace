# gui/components/chart.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure


class DonutChart(QWidget):
    def __init__(self, percent, label):
        super().__init__()

        figure = Figure(figsize=(2, 2))
        canvas = Canvas(figure)
        ax = figure.add_subplot(111)

        # Draw donut chart
        val = min(percent, 100)
        colors = ["#4CAF50", "#FF9800", "#f44336"]  # green, orange, red
        color = (
            colors[0] if percent < 80 else
            colors[1] if percent <= 100 else
            colors[2]
        )

        ax.pie([val, 100 - val], colors=[color, "#e0e0e0"], startangle=90, wedgeprops=dict(width=0.3))
        ax.text(0, 0, f"{percent:.0f}%", ha='center', va='center', fontsize=14)

        ax.set_aspect('equal')
        ax.axis('off')

        layout = QVBoxLayout()
        layout.addWidget(canvas)
        canvas.draw()
        self.setLayout(layout)
