import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

from impressive_ui.qt import MutableState
from impressive import apply


def Counter() -> QWidget:
    count = MutableState(0)

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setSpacing(6)

    @apply(layout.addWidget)
    def _():
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        count.map(str).bind(label, "text")
        return label

    @apply(layout.addWidget)
    def _():
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(12)

        @apply(button_layout.addWidget).foreach
        def _():
            button_remove = QPushButton("-")
            button_remove.setFixedSize(40, 40)
            button_remove.clicked.connect(lambda: count.update(lambda x: x - 1))

            button_reset = QPushButton("Reset")
            button_reset.setFixedSize(60, 40)
            button_reset.clicked.connect(lambda: count.set(0))

            button_add = QPushButton("+")
            button_add.setFixedSize(40, 40)
            button_add.clicked.connect(lambda: count.update(lambda x: x + 1))

            return (
                button_remove,
                button_reset,
                button_add,
            )

        return button_widget

    return widget


def Window() -> QMainWindow:
    window = QMainWindow()
    window.setWindowTitle("Counter App")
    window.setFixedSize(300, 400)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    layout = QVBoxLayout(central_widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    counter_widget = Counter()
    layout.addWidget(counter_widget)
    
    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Window()
    window.show()
    
    sys.exit(app.exec())