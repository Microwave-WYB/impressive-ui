# Impressive UI

⚠️ **Not Release Ready**: This project is in active development and is not ready for release. APIs may change significantly and breaking changes are expected. Not recommended for production use.

An (almost) declarative, reactive UI framework for Python applications, built on top of the [impressive](https://github.com/Microwave-WYB/impressive) DSL library. Impressive UI transforms traditional imperative UI programming into an expressive, functional approach with automatic state management and reactive data binding.

Currently supports both GTK and Qt with PySide6.

## Installation

For GTK:

```sh
pip install git+https://github.com/Microwave-WYB/impressive-ui.git[gtk]
```

For Qt:

```sh
pip install git+https://github.com/Microwave-WYB/impressive-ui.git[qt]
```

## Quick Start

### GTK Example

```python
import gi
from impressive_ui.gtk import MutableState
from impressive import apply

gi.require_versions({"Gtk": "4.0", "Adw": "1"})
from gi.repository import Adw, Gtk

def HelloWorld():
    name = MutableState("")

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

    @apply(box.append)
    def _():
        entry = Gtk.Entry(placeholder_text="Enter your name...")
        name.bind_twoway(entry, "text")
        return entry

    @apply(box.append)
    def _():
        label = Gtk.Label(css_classes=["title-1"])
        name.map(lambda x: f"Hello, {x or '...'}!").bind(label, "label")
        return label

    return box

if __name__ == "__main__":
    app = Adw.Application()
    app.connect("activate", lambda app: Adw.ApplicationWindow(
        application=app, content=HelloWorld()
    ).present())
    app.run([])
```

### Qt Example

```python
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)
from PySide6.QtCore import Qt

from impressive_ui.qt import MutableState, qss
from impressive import apply

def HelloWorld():
    # Create reactive state
    name = MutableState("")

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.setSpacing(12)

    @apply(layout.addWidget)
    def _():
        entry = QLineEdit()
        entry.setPlaceholderText("Enter your name...")
        entry.setFixedWidth(200)
        # Manual two-way binding using watch and signals
        name.watch(lambda text: entry.setText(text) if entry.text() != text else None)
        entry.textChanged.connect(name.set)
        entry.returnPressed.connect(
            lambda: print(f"Entry activated with text: {name._value}")
        )
        return entry

    @apply(layout.addWidget)
    def _():
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use watch pattern to update label
        greeting = name.map(lambda x: f"Hello, {x or '...'}!")
        greeting.watch(lambda text: label.setText(text))
        return label

    return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Hello Impressive Qt")
    window.setFixedSize(450, 250)

    # Beautiful gradient styling - combine stylesheets with +
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

    central_widget = HelloWorld()
    window.setCentralWidget(central_widget)

    window.show()

    sys.exit(app.exec())
```

## Why Impressive UI?

Traditional UI programming requires manual state management, explicit event handling, and imperative DOM manipulation. Impressive UI provides:

- **Reactive State Management**: Automatic UI updates when state changes
- **Type Safety**: Full generic type support with proper inference
- **Declarative Patterns**: Compose UIs with functional programming
- **Framework-Optimized**: GTK gets property binding, Qt uses efficient watch patterns
- **Modern Styling**: CSS-like styling with Python syntax (Qt)

## Core Concepts

### State Management

Both GTK and Qt implementations provide reactive state management:

```python
# Create mutable reactive state
counter = MutableState(0)

# Read current value
print(counter.value)  # 0
print(counter.get())  # 0

# Update state
counter.set(5)
counter.update(lambda x: x + 1)

# Create derived state
doubled = counter.map(lambda x: x * 2)
is_positive = counter.map(lambda x: x > 0)

# Watch for changes
unwatch = counter.watch(lambda value: print(f"Count: {value}"))
unwatch()  # Stop watching
```

### Framework-Specific Binding

**GTK - Built-in Property Binding:**
```python
# One-way binding (property name only)
text_state.bind(label, "label")

# Two-way binding
entry_text.bind_twoway(entry, "text")
```

**Qt - Watch Pattern:**
```python
# One-way binding using watch
text_state.watch(lambda text: label.setText(text))
# Or using property
text_state.watch(lambda text: label.setProperty("text", text))

# Manual two-way binding
text_state.watch(lambda text: entry.setText(text) if entry.text() != text else None)
entry.textChanged.connect(text_state.set)
```

### The `@apply` Decorator

The `@apply` decorator enables powerful composition patterns:

```python
# Simple widget creation
@apply(layout.addWidget)  # Qt
@apply(box.append)        # GTK
def _():
    button = QPushButton("Click me")  # or Gtk.Button()
    button.clicked.connect(on_click)
    return button

# Multiple widgets
@apply(layout.addWidget).foreach
def _():
    return (
        QPushButton("Button 1"),
        QPushButton("Button 2"),
        QPushButton("Button 3"),
    )
```

## Qt-Specific Features

### Styling System

Qt implementation includes a powerful CSS-in-Python styling system using `qss`:

```python
from impressive_ui.qt import qss

# Inline styles (no selector) - for direct widget.setStyleSheet()
label = QLabel("Styled text")
label.setStyleSheet(qss(
    font_size="18px",
    color="#333",
    padding="10px",
    background_color="#f0f0f0",
    border_radius="6px"
))

# Selector-based styles - qss[...] compiles to string
window.setStyleSheet(qss[QPushButton](
    background_color="#3498db",
    color="white",
    border="none",
    padding="8px 16px"
))

# Hover effects
button.setStyleSheet(qss["QPushButton:hover"](
    background_color="#2980b9"
))

# Multiple selectors
container.setStyleSheet(qss[(QLabel, QPushButton)](
    font_family="Arial, sans-serif"
))

# Combine stylesheets with simple string concatenation
window.setStyleSheet(
    qss[QMainWindow](background_color="#f0f0f0") +
    qss[QPushButton](color="blue") +
    qss[QLabel](font_weight="bold")
)
```

#### Available Style Properties

- **Layout**: `width`, `height`, `margin`, `padding`, `min_width`, `max_height`
- **Colors**: `color`, `background_color`, `border_color`
- **Typography**: `font_family`, `font_size`, `font_weight`, `text_align`
- **Borders**: `border`, `border_radius`, `border_style`, `border_width`
- **Effects**: `background` (gradients), `text_decoration`

Python property names are automatically converted to CSS (e.g., `background_color` → `background-color`).

## GTK-Specific Features

### Factories

GTK implementation provides high-level factory functions:

#### ReactiveSequence

Automatically manage dynamic lists of widgets:

```python
from impressive_ui.gtk import ReactiveSequence

tasks = MutableState([
    TaskViewModel("Buy groceries"),
    TaskViewModel("Walk the dog"),
])

task_list = ReactiveSequence(
    Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE),
    tasks,
    lambda task: TaskWidget(task, on_remove=remove_task)
)
```

#### Conditional

Conditionally render widgets based on state:

```python
from impressive_ui.gtk import Conditional

has_tasks = tasks.map(lambda t: len(t) > 0)

content = Conditional(
    has_tasks,
    true=task_list,
    false=Gtk.Label(label="No tasks yet")
)
```

#### Preview

Rapid prototyping and component development:

```python
from impressive_ui.gtk import Preview

if __name__ == "__main__":
    preview = Preview()

    @preview("MyWidget")
    def _(args) -> Gtk.Widget:
        return MyCustomWidget()

    preview.run()
```

### Traditional vs Declarative

**Traditional GTK:**
```python
class HelloWorldWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.name = ""

        self.entry = Gtk.Entry()
        self.entry.connect("changed", self._on_entry_changed)
        self.append(self.entry)

        self.label = Gtk.Label()
        self._update_label()
        self.append(self.label)

    def _on_entry_changed(self, entry):
        self.name = entry.get_text()
        self._update_label()

    def _update_label(self):
        self.label.set_text(f"Hello, {self.name or '...'}!")
```

**Impressive UI GTK:**
```python
def HelloWorld():
    name = MutableState("")

    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    @apply(box.append)
    def _():
        entry = Gtk.Entry()
        name.bind_twoway(entry, "text")
        return entry

    @apply(box.append)
    def _():
        label = Gtk.Label()
        name.map(lambda x: f"Hello, {x or '...'}!").bind(label, "label")
        return label

    return box
```

**Impressive UI Qt:**
```python
def HelloWorld():
    name = MutableState("")

    widget = QWidget()
    layout = QVBoxLayout(widget)

    @apply(layout.addWidget)
    def _():
        entry = QLineEdit()
        name.watch(lambda text: entry.setText(text) if entry.text() != text else None)
        entry.textChanged.connect(name.set)
        return entry

    @apply(layout.addWidget)
    def _():
        label = QLabel()
        greeting = name.map(lambda x: f"Hello, {x or '...'}!")
        greeting.watch(lambda text: label.setText(text))
        return label

    return widget
```

## Examples

### GTK Examples

Run GTK examples from the repository:

```bash
python examples/gtk/hello.py      # Basic hello world
python examples/gtk/counter.py    # Interactive counter
python examples/gtk/todo.py       # Todo application
python examples/gtk/calc.py       # Calculator with MVVM
```

### Qt Examples

Run Qt examples from the repository:

```bash
python examples/qt/hello.py       # Beautiful hello world
python examples/qt/counter.py     # Interactive counter
python examples/qt/test_style.py  # Styling demonstration
```

## Best Practices

1. **Single Source of Truth**: Keep state centralized and flow data down
2. **Pure Functions**: Use pure functions for state transformations
3. **Immutable Updates**: Always create new state rather than mutating
4. **Component Composition**: Break UI into small, reusable components
5. **Reactive Patterns**: Let state changes drive UI updates automatically

## Design Patterns

### MVVM (Model-View-ViewModel)

Recommended pattern for complex applications:

```python
class TodoViewModel:
    def __init__(self):
        self._tasks = MutableState([])
        self._entry_text = MutableState("")

    @property
    def tasks(self):
        return self._tasks

    @property
    def entry_text(self):
        return self._entry_text

    def add_task(self):
        text = self._entry_text.value.strip()
        if text:
            new_task = TaskModel(text)
            self._tasks.update(lambda ts: [*ts, new_task])
            self._entry_text.set("")

def TodoView(view_model):
    # UI components that bind to view model state
    pass
```

### State Composition

```python
class AppState:
    def __init__(self):
        self.user = MutableState(None)
        self.theme = MutableState("light")
        self.notifications = MutableState([])

    @property
    def is_logged_in(self):
        return self.user.map(lambda u: u is not None)
```

## API Reference

### State Classes

#### `State[T]` (Base class)
- `get() -> T` - Get current state value
- `value: T` - Current state value (property)
- `watch(callback: (T) -> Any) -> (() -> None)` - Watch for changes
- `map(mapper: (T) -> U) -> State[U]` - Create derived state

#### `MutableState[T]` (extends State[T])
- `set(value: T) -> None` - Set new value
- `update(updater: (T) -> T) -> None` - Update with function

#### GTK-Specific Methods
- `bind(target: Widget, property: str) -> Binding` - One-way property binding
- `bind_twoway(target: Widget, property: str) -> Binding` - Two-way property binding

#### Qt-Specific Pattern
- Use `watch()` method for all UI updates - no built-in binding methods

### qss Styling (Qt only)

#### `qss`
- `qss(**properties) -> str` - Create inline stylesheet (no selector)
- `qss[selector](**properties) -> str` - Create stylesheet with selector
- Supports widget types, tuples of types, or string selectors
- Results are strings that can be combined with `+` operator
- Python property names automatically convert to CSS (e.g., `background_color` → `background-color`)

## Type Safety

Full generic type support with proper inference:

```python
# Type is inferred as MutableState[int]
count = MutableState(0)

# Type is inferred as State[str]
count_text = count.map(str)

# Type is inferred as State[bool]
is_positive = count.map(lambda x: x > 0)
```

## Contributing

Contributions are welcome! Please see the repository for guidelines.

## License

This project is licensed under the MIT License.
