from collections.abc import Callable
from typing import Any, Generic, TypeVar, TYPE_CHECKING
from gi.repository import GLib, GObject  # type: ignore

if TYPE_CHECKING:
    from impressive_ui.abc.state import (
        check_state_impl,
        check_mutable_state_impl,
    )

T = TypeVar("T")
U = TypeVar("U")


class GtkStateObject(GObject.GObject, Generic[T]):
    """
    A base class for GTK state objects that can be used with GObject properties.
    This class is not meant to be instantiated directly.
    """

    value: T = GObject.Property(type=object)  # type: ignore

    def __init__(self, initial_value: T) -> None:
        super().__init__()
        self.value = initial_value


class State(Generic[T]):
    def __init__(self, initial_value: T) -> None:
        self._obj = GtkStateObject(initial_value)

    @property
    def value(self) -> T:
        """
        The current state value.
        This property is used to access the value of the state.
        """
        return self._obj.value

    def get(self) -> T:
        return self.value

    def watch(self, callback: Callable[[T], Any]) -> Callable[[], None]:
        callback(self._obj.value)
        connection = self._obj.connect(
            "notify::value", lambda *_: callback(self._obj.value)
        )
        return lambda: self._obj.disconnect(connection)

    def bind(self, target: GObject.Object, property_name: str) -> GObject.Binding:
        """
        Bind this state to a GObject property using GTK's property binding system.
        """
        return self._obj.bind_property(
            "value",
            target,
            property_name,
            GObject.BindingFlags.SYNC_CREATE,
            lambda binding, value: value,
            lambda binding, value: value,
        )

    def map(self, mapper: Callable[[T], U], /) -> "State[U]":
        derived = MutableState(mapper(self._obj.value))
        self.watch(lambda v: derived.set(mapper(v)))
        return derived


if TYPE_CHECKING:
    check_state_impl(State)


class MutableState(State[T]):
    def set(self, value: T) -> None:
        GLib.idle_add(lambda: setattr(self._obj, "value", value))

    def update(self, updater: Callable[[T], T]) -> None:
        self.set(updater(self._obj.value))

    def bind_twoway(self, target: GObject.Object, property_name: str) -> Any:
        binding = self._obj.bind_property(
            "value",
            target,
            property_name,
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
            lambda binding, value: value,
            lambda binding, value: value,
        )
        return binding


if TYPE_CHECKING:
    check_mutable_state_impl(MutableState)
