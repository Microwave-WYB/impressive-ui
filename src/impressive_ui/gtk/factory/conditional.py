from gi.repository import Gtk  # type: ignore
from impressive_ui.abc.state import AbstractState


def Conditional(
    state: AbstractState[bool],
    true: Gtk.Widget,
    false: Gtk.Widget,
) -> Gtk.Overlay:
    """
    Create a Gtk.Overlay that conditionally shows one of two widgets based on the state.
    """
    overlay = Gtk.Overlay()
    state.map(lambda condition: true if condition else false).bind(overlay, "child")
    return overlay
