from collections.abc import Callable
from typing import Any, Generic, TypeVar, TYPE_CHECKING
from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from impressive_ui.abc.state import (
        check_state_impl,
        check_mutable_state_impl,
    )

T = TypeVar("T")
U = TypeVar("U")


class State(QObject, Generic[T]):
    valueChanged = Signal(object)

    def __init__(self, initial_value: T) -> None:
        super().__init__()
        self._value = initial_value

    def get(self) -> T:
        return self._value

    @property
    def value(self) -> T:
        return self._value

    def watch(self, callback: Callable[[T], Any]) -> Callable[[], None]:
        callback(self._value)  # Call immediately with current value
        self.valueChanged.connect(callback)

        def disconnect_callback() -> None:
            self.valueChanged.disconnect(callback)

        return disconnect_callback

    def map(self, mapper: Callable[[T], U], /) -> "State[U]":
        derived = MutableState(mapper(self._value))
        self.watch(lambda v: derived.set(mapper(v)))
        return derived


if TYPE_CHECKING:
    check_state_impl(State)


class MutableState(State[T], Generic[T]):
    def set(self, value: T) -> None:
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)

    def update(self, updater: Callable[[T], T]) -> None:
        new_value = updater(self._value)
        self.set(new_value)


if TYPE_CHECKING:
    check_mutable_state_impl(MutableState)
