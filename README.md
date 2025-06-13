# Impressive UI

⚠️ **Not Release Ready**: This project is in active development and is not ready for release. APIs may change significantly and breaking changes are expected. Not recommended for production use.

An (almost) declarative, reactive UI framework for Python applications, built on top of the [impressive](https://github.com/Microwave-WYB/impressive) DSL library. Impressive UI transforms traditional imperative UI programming into an expressive, functional approach with automatic state management and reactive data binding.

Currently supports GTK with Qt support planned.

## Installation

For GTK:

```sh
pip install git+https://github.com/Microwave-WYB/impressive-ui.git[gtk]
```

For Qt (not yet available):

```sh
pip install git+https://github.com/Microwave-WYB/impressive-ui.git[qt]
```

## Why Impressive UI?

Traditional UI programming requires manual state management, explicit event handling, and imperative DOM manipulation. Impressive UI leverages the power of the `impressive` DSL to provide a declarative alternative that's more maintainable and expressive.

## GTK

### Getting Started with GTK

Traditional GTK programming requires manual state management, explicit event handling, and imperative widget manipulation. Impressive UI for GTK provides a declarative alternative that's more maintainable and expressive.

#### Traditional vs Declarative

**Traditional GTK approach:**

```python
class HelloWorldWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        self.name = ""

        self.entry = Gtk.Entry(placeholder_text="Enter your name...")
        self.entry.connect("activate", self._on_entry_activate)
        self.entry.connect("changed", self._on_entry_changed)
        self.append(self.entry)

        self.label = Gtk.Label(css_classes=["title-1"])
        self._update_label()
        self.append(self.label)

    def _on_entry_changed(self, entry):
        self.name = entry.get_text()
        self._update_label()

    def _update_label(self):
        self.label.set_text(f"Hello, {self.name or '...'}!")
```

**Impressive UI declarative approach:**

```python
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
```

The declarative approach eliminates boilerplate, automatically handles state synchronization, and makes the component's data flow explicit and easy to reason about.

### Core Concepts

#### State Management

Impressive UI provides reactive state management through `MutableState` and `State` objects:

```python
from impressive_ui.gtk import MutableState, State

# Create mutable reactive state
counter = MutableState(0)

# Create derived state
is_even = counter.map(lambda x: x % 2 == 0)

# Update state
counter.set(5)
counter.update(lambda x: x + 1)

# Watch state changes
@counter.watch
def _(value):
    print(f"Counter changed to: {value}")
```

#### Property Binding

Bind state directly to GTK widget properties:

```python
# One-way binding: state → widget
text_state = MutableState("Hello")
label = Gtk.Label()
text_state.bind(label, "label")

# Two-way binding: state ↔ widget
entry_text = MutableState("")
entry = Gtk.Entry()
entry_text.bind_twoway(entry, "text")
```

#### The `@apply` Decorator

The `@apply` decorator from the `impressive` library enables powerful composition patterns. **Note:** Apply-decorated functions are executed immediately, and their return value is passed as an argument to the function specified in `apply()`.

Here are the key patterns and best practices:

##### Simple `apply`

Use for individual widgets with complex setup:

```python
@apply(box.append)
def _():
    button = Gtk.Button(label="Click me")
    button.connect("clicked", on_complex_action)
    button.add_css_class("special-button")
    return button
```

##### `apply` with `foreach`

**Best practice:** Use `foreach` when setting up multiple widgets with similar configurations:

```python
@apply(box.append).foreach
def _():
    return (
        Gtk.Button(label="Button 1"),
        Gtk.Button(label="Button 2"),
        Gtk.Button(label="Button 3"),
    )
```

##### Individual `apply` vs `foreach`

Choose based on complexity:

```python
# Complex widgets with different setups - use individual apply
@apply(toolbar.append)
def _():
    save_button = Gtk.Button(icon_name="document-save")
    save_button.connect("clicked", save_document)
    save_button.set_tooltip_text("Save document")
    return save_button

@apply(toolbar.append)
def _():
    menu_button = Gtk.MenuButton()
    menu_button.set_popover(create_menu_popover())
    menu_button.set_icon_name("open-menu")
    return menu_button

# Simple widgets with similar setups - use foreach
@apply(button_box.append).foreach
def _():
    return (
        Gtk.Button(label="OK"),
        Gtk.Button(label="Cancel"),
        Gtk.Button(label="Apply"),
    )
```

##### `apply.unpack_to`

Use `unpack_to` individually for single widgets with positional arguments:

```python
@apply.unpack_to(grid.attach)
def _():
    return (Gtk.Button(label="Center"), 1, 1, 1, 1)  # widget, left, top, width, height
```

##### Apply Unpack To Foreach

Use for multiple widgets that need positional arguments:

```python
@apply.unpack_to(grid.attach).foreach
def _():
    return (
        (Gtk.Button(label="0"), 0, 0, 1, 1),
        (Gtk.Button(label="1"), 1, 0, 1, 1),
        (Gtk.Button(label="2"), 2, 0, 1, 1),
    )
```

For complex grid layouts:

```python
@apply.unpack_to(grid.attach).foreach
def _():
    buttons = []
    for i in range(10):
        row, col = divmod(i, 3)
        buttons.append((
            Gtk.Button(label=str(i)),
            col, row, 1, 1
        ))
    return buttons
```

### Factories

Impressive UI provides high-level factory functions for common patterns:

#### ReactiveSequence

Automatically manage dynamic lists of widgets:

```python
from impressive_ui.gtk import ReactiveSequence

tasks = MutableState([
    TaskViewModel("Buy groceries"),
    TaskViewModel("Walk the dog"),
    TaskViewModel("Write code"),
])

task_list = ReactiveSequence(
    Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE),
    tasks,
    lambda task: TaskWidget(task, on_remove=remove_task)
)
```

The `ReactiveSequence` automatically:
- Adds widgets when items are added to the state
- Removes widgets when items are removed
- Maintains efficient updates with minimal DOM manipulation

#### Conditional

Conditionally render widgets based on state:

```python
from impressive_ui.gtk import Conditional

has_tasks = tasks.map(lambda t: len(t) > 0)

content = Conditional(
    has_tasks,
    true=task_list,
    false=Gtk.Label(label="No tasks yet", css_classes=["dim-label"])
)
```

#### Preview

The `Preview` factory enables rapid prototyping and component development:

```python
from impressive_ui.gtk import Preview

if __name__ == "__main__":
    preview = Preview()

    @preview("TaskWidget")
    def _(args) -> Gtk.Widget:
        sample_task = TaskViewModel("Sample Task")
        return TaskWidget(sample_task, lambda t: print(f"Remove: {t.title}"))

    @preview("Calculator")
    def _(args) -> Adw.Window:
        return CalculatorWindow()

    preview.run()
```

Run the script and select which component to preview from a simple interface.

### Real-World Examples

**Recommended Design Pattern:** MVVM (Model-View-ViewModel) works exceptionally well with Impressive UI's reactive architecture. See [`examples/gtk/calc.py`](examples/gtk/calc.py) for a comprehensive example of this pattern in practice.

#### Todo Application

A complete todo app demonstrating state management, two-way binding, and reactive lists:

```python
class TodoViewModel:
    def __init__(self):
        self._tasks = MutableState([])
        self._entry_text = MutableState("")

    def add_task(self):
        text = self._entry_text.value.strip()
        if text:
            new_task = TaskViewModel(text)
            self._tasks.update(lambda ts: [*ts, new_task])
            self._entry_text.set("")

def TaskList(tasks, on_remove):
    return Conditional(
        tasks.map(bool),
        true=ReactiveSequence(
            Gtk.ListBox(css_classes=["boxed-list"]),
            tasks,
            lambda task: TaskWidget(task, on_remove=on_remove)
        ),
        false=Gtk.Label(label="No tasks yet", css_classes=["dim-label"])
    )
```

#### Calculator

A functional calculator with keyboard support and error handling:

```python
class CalculatorViewModel:
    def __init__(self):
        self._state = MutableState(CalculatorModel())

    def enter(self, action):
        self._state.update(lambda state: state.update(action))

def ResultsDisplay(view_model):
    # Reactive display that automatically updates
    result_label = Gtk.Label(css_classes=["title-1"])
    view_model.state.map(lambda s: s.result).bind(result_label, "label")

    # Conditional styling based on error state
    @view_model.state.map(lambda s: s.error).watch
    def _(has_error):
        if has_error:
            result_label.add_css_class("error")
        else:
            result_label.remove_css_class("error")
```

## Qt

Qt support is planned for future releases.

## Getting Started

1. Import the necessary modules
2. Create your state with `MutableState`
3. Build your UI with the `@apply` decorator
4. Use factories like `ReactiveSequence` and `Conditional` for dynamic content
5. Bind state to widget properties for automatic updates

The combination of reactive state management, declarative composition with `@apply`, and powerful factories makes building complex GTK applications both enjoyable and maintainable.
