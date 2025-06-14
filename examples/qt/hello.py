import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import Qt

from impressive_ui.qt import MutableState, qss, container
from impressive import apply


def HelloWorld():
    # Create reactive state
    name = MutableState("")

    widget, layout = container(QVBoxLayout)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setSpacing(12)

    @apply(layout.addWidget).foreach
    def _():
        entry = QLineEdit()
        entry.setPlaceholderText("Enter your name...")
        entry.setFixedWidth(200)
        entry.textChanged.connect(name.set)
        entry.returnPressed.connect(
            lambda: print(f"Entry activated with text: {name._value}")
        )
        yield entry

        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name.map(lambda x: f"Hello, {x or '...'}!").watch(label.setText)
        yield label

    return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Hello Impressive Qt")
    window.setFixedSize(450, 250)

    window.setStyleSheet(
        qss[QMainWindow](
            background_color="qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f8bbd9, stop:0.5 #e8eaf6, stop:1 #c8e6c9)",
            font_family="SF Pro Display, system-ui, sans-serif",
        )
        + qss[QLabel](
            font_size="28px",
            font_weight="600",
            color="#4a148c",
            padding="16px 24px",
            background_color="qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f3e5f5, stop:1 #e8eaf6)",
            border="2px solid #ce93d8",
            border_radius="16px",
            font_family="SF Pro Display, system-ui, sans-serif",
            text_align="center",
        )
        + qss[QLineEdit](
            padding="12px 16px",
            border="2px solid #e1bee7",
            border_radius="12px",
            font_size="16px",
            background_color="#fce4ec",
            color="#6a1b9a",
            font_family="SF Pro Display, system-ui, sans-serif",
        )
    )

    window.setCentralWidget(HelloWorld())
    window.show()
    app.exec()
