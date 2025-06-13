from collections.abc import Callable, Sequence
from typing import Any, TypeVar, overload

import gi


from impressive_ui.gtk.state import State
from impressive_ui.reactive_sequence import bind_sequence, insert_widget, remove_widget

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk  # type: ignore # noqa: E402


@insert_widget.register
def _(container: Gtk.ListBox, widget: Gtk.Widget, index: int) -> None:
    if widget.get_parent() is not None:
        widget.unparent()
    container.insert(widget, index)


@insert_widget.register
def _(container: Gtk.Box, widget: Gtk.Widget, index: int) -> None:
    if index == 0:
        container.prepend(widget)
    else:
        current_child = container.get_first_child()
        for _ in range(index - 1):
            if current_child:
                current_child = current_child.get_next_sibling()
            else:
                break

        if current_child:
            container.insert_child_after(widget, current_child)
        else:
            container.append(widget)


@insert_widget.register
def _(container: Gtk.FlowBox, widget: Gtk.Widget, index: int) -> None:
    if widget.get_parent() is not None:
        widget.unparent()
    container.insert(widget, index)


@remove_widget.register
def _(container, widget: Gtk.Widget) -> None:
    container.remove(widget)


def Conditional(
    state: State[bool],
    true: Gtk.Widget,
    false: Gtk.Widget,
) -> Gtk.Overlay:
    """Create a Gtk.Overlay that conditionally shows one of two widgets based on the state."""
    overlay = Gtk.Overlay()
    state.map(lambda condition: true if condition else false).bind(overlay, "child")
    return overlay


ItemT = TypeVar("ItemT")
KeyT = TypeVar("KeyT")


@overload
def ReactiveSequence(
    container: Gtk.Box,
    items: State[Sequence[ItemT]],
    factory: Callable[[ItemT], Gtk.Widget],
    *,
    key_fn: Callable[[ItemT], KeyT] = id,
) -> Gtk.Box: ...


@overload
def ReactiveSequence(
    container: Gtk.ListBox,
    items: State[Sequence[ItemT]],
    factory: Callable[[ItemT], Gtk.ListBoxRow],
    *,
    key_fn: Callable[[ItemT], KeyT] = id,
) -> Gtk.ListBox: ...


@overload
def ReactiveSequence(
    container: Gtk.FlowBox,
    items: State[Sequence[ItemT]],
    factory: Callable[[ItemT], Gtk.FlowBoxChild],
    *,
    key_fn: Callable[[ItemT], KeyT] = id,
) -> Gtk.FlowBox: ...


def ReactiveSequence(
    container,
    items: State[Sequence[ItemT]],
    factory: Callable[[ItemT], Any],
    *,
    key_fn: Callable[[ItemT], KeyT] = id,
) -> Gtk.Widget:
    """Bind a sequence state to a GTK container with efficient diff updates."""
    bind_sequence(container, items, key_fn=key_fn)(factory)
    return container
