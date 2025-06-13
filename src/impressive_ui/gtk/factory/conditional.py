from gi.repository import Gtk  # type: ignore
from impressive_ui.gtk.state import State


def Conditional(
    state: State[bool],
    true: Gtk.Widget,
    false: Gtk.Widget,
) -> Gtk.Overlay:
    """
    Create a Gtk.Overlay that conditionally shows one of two widgets based on the state.
    """
    overlay = Gtk.Overlay()
    
    def update_child(condition: bool) -> None:
        overlay.set_child(true if condition else false)
    
    state.watch(update_child)
    return overlay
