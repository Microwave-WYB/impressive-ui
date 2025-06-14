from typing import TypeVar
from PySide6.QtWidgets import QLayout, QWidget

T = TypeVar("T", bound=QLayout)


def container(layout_type: type[T]) -> tuple[QWidget, T]:
    """Create a widget with a layout."""
    widget, layout = QWidget(), layout_type()
    widget.setLayout(layout)
    return widget, layout
