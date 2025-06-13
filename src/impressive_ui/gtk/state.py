from collections.abc import Callable
from typing import Any, Generic, TypeVar, TYPE_CHECKING
from gi.repository import GObject  # type: ignore

if TYPE_CHECKING:
    from impressive_ui.abc.state import (
        check_state_impl,
        check_mutable_state_impl,
    )
    from impressive_ui.abc import AbstractState

T = TypeVar("T")
U = TypeVar("U")


# GObject doesn't support multiple inheritance
# So we use check_state_impl and check_mutable_state_impl for implementation checks
class State(GObject.GObject, Generic[T]):
    value = GObject.Property(type=object)

    def __init__(self, initial_value: T) -> None:
        super().__init__()
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


if TYPE_CHECKING:
    # ensure State implements AbstractState
    check_state_impl(State)


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


if TYPE_CHECKING:
    # ensure MutableState implements AbstractMutableState
    check_mutable_state_impl(MutableState)
