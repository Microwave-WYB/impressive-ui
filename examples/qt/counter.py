import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Qt

from impressive_ui.qt import MutableState, container, qss
from impressive import apply


def Counter() -> QWidget:
    count = MutableState(0)

    counter, layout = container(QVBoxLayout)

    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setSpacing(6)

    @apply(layout.addWidget)
    def _():
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(qss(font_size="24px", font_weight="bold"))
        count.map(str).watch(lambda text: label.setText(text))
        return label

    @apply(layout.addLayout)
    def _():
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)

        @apply(layout.addWidget).foreach
        def _():
            button_remove = QPushButton("-")
            button_remove.setFixedSize(40, 40)
            button_remove.clicked.connect(lambda: count.update(lambda x: x - 1))
            yield button_remove

            button_reset = QPushButton("Reset")
            button_reset.setFixedSize(60, 40)
            button_reset.clicked.connect(lambda: count.set(0))
            yield button_reset

            button_add = QPushButton("+")
            button_add.setFixedSize(40, 40)
            button_add.clicked.connect(lambda: count.update(lambda x: x + 1))
            yield button_add

        return layout

    return counter


def Window() -> QMainWindow:
    window = QMainWindow()
    window.setWindowTitle("Counter App")
    window.setFixedSize(300, 400)

    @apply(window.setCentralWidget)
    def _():
        widget, layout = container(QVBoxLayout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(12)
        layout.addWidget(Counter())
        return widget

    return window


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())
