from collections.abc import Callable, Iterator, Sequence
from typing import Any, TypeVar, overload

import gi


from impressive_ui.gtk import State
from impressive_ui.reactive_sequence import insert_widget, remove_widget, diff_update

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk  # type: ignore # noqa: E402

ItemT = TypeVar("ItemT")
KeyT = TypeVar("KeyT", bound=Any)


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

    # Use a dict to store mutable state
    state = {"current_items": tuple(), "widget_by_key": {}}

    def get_container_widgets() -> Iterator[Gtk.Widget]:
        """Get current widgets in container in order."""
        child = container.get_first_child()
        while child:
            yield child
            child = child.get_next_sibling()

    def remove_widget_from_container(widget: Gtk.Widget) -> None:
        """Remove widget from container and clean up tracking."""
        remove_widget(container, widget)

        # Remove from tracking dict
        for key, tracked_widget in list(state["widget_by_key"].items()):
            if tracked_widget is widget:
                del state["widget_by_key"][key]
                break

    def insert_widget_in_container(widget: Gtk.Widget, position: int) -> None:
        """Insert widget at position in container."""
        insert_widget(container, widget, position)

    def create_and_track_widget(item: ItemT) -> Gtk.Widget:
        """Create widget and track it by key."""
        widget = factory(item)
        state["widget_by_key"][key_fn(item)] = widget
        return widget

    @items.watch
    def sync_items(new_items: Sequence[ItemT]):
        """Sync container using efficient diff algorithm."""

        diff_update(
            container=None,  # We don't actually need this if we pass functions directly
            old_source=state["current_items"],
            new_source=new_items,
            key_func=key_fn,
            factory=create_and_track_widget,
            remove=lambda _container, widget: remove_widget_from_container(widget),
            insert=lambda _container, widget, pos: insert_widget_in_container(
                widget, pos
            ),
            get_container_items=lambda _container: tuple(get_container_widgets()),
        )

        state["current_items"] = new_items

    return container
