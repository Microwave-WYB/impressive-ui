from collections.abc import Callable
from typing import Any, Generic, TypeVar, TYPE_CHECKING
from gi.repository import GObject  # type: ignore

if TYPE_CHECKING:
    from impressive_ui.abc import AbstractState

T = TypeVar("T")
U = TypeVar("U")


class State(GObject.GObject, Generic[T]):
    value = GObject.Property(type=object)

    def __init__(self, initial_value: T) -> None:
        GObject.GObject.__init__(self)
        self.value = initial_value

    def watch(self, callback: Callable[[T], Any]) -> Callable[[], None]:
        callback(self.value)  # Call immediately with current value
        connection = self.connect("notify::value", lambda *_: callback(self.value))
        return lambda: self.disconnect(connection)

    def map(self, mapper: Callable[[T], U], /) -> "AbstractState[U]":
        derived = MutableState(mapper(self.value))
        self.watch(lambda v: derived.set(mapper(v)))
        return derived

    def bind(self, target: GObject.Object, property_name: str) -> GObject.Binding:
        return self.bind_property(
            "value",
            target,
            property_name,
            GObject.BindingFlags.SYNC_CREATE,
            lambda binding, value: value,
            lambda binding, value: value,
        )


class MutableState(State[T], Generic[T]):
    def set(self, value: T) -> None:
        self.value = value

    def update(self, updater: Callable[[T], T]) -> None:
        self.value = updater(self.value)

    def bind_twoway(self, target: GObject.Object, property_name: str) -> Any:
        binding = self.bind_property(
            "value",
            target,
            property_name,
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL,
            lambda binding, value: value,
            lambda binding, value: value,
        )
        return binding
