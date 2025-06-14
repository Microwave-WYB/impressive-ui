from collections.abc import Callable
from typing import Any, Generic, TypeVar, TYPE_CHECKING
from PySide6.QtCore import QObject, Signal, QTimer

if TYPE_CHECKING:
    from impressive_ui.abc.state import (
        check_state_impl,
        check_mutable_state_impl,
    )

T = TypeVar("T")
U = TypeVar("U")


class QtStateObject(QObject, Generic[T]):
    """
    A base class for Qt state objects that can be used with QObject signals.
    This class is not meant to be instantiated directly.
    """

    valueChanged = Signal(object)

    def __init__(self, initial_value: T) -> None:
        super().__init__()
        self._value = initial_value

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: T) -> None:
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(new_value)


class State(Generic[T]):
    def __init__(self, initial_value: T) -> None:
        self._obj = QtStateObject(initial_value)

    def get(self) -> T:
        return self._obj.value

    @property
    def value(self) -> T:
        """
        The current state value.
        This property is used to access the value of the state.
        """
        return self._obj.value

    def watch(self, callback: Callable[[T], Any]) -> Callable[[], None]:
        callback(self._obj.value)  # Call immediately with current value
        self._obj.valueChanged.connect(callback)

        def disconnect_callback() -> None:
            self._obj.valueChanged.disconnect(callback)

        return disconnect_callback

    def map(self, mapper: Callable[[T], U], /) -> "State[U]":
        derived = MutableState(mapper(self._obj.value))
        self.watch(lambda v: derived.set(mapper(v)))
        return derived


if TYPE_CHECKING:
    check_state_impl(State)


class MutableState(State[T]):
    def set(self, value: T) -> None:
        QTimer.singleShot(0, lambda: setattr(self._obj, "value", value))

    def update(self, updater: Callable[[T], T]) -> None:
        self.set(updater(self._obj.value))


if TYPE_CHECKING:
    check_mutable_state_impl(MutableState)
