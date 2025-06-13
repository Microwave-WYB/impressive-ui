from typing import Any, Callable, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
U = TypeVar("U")
T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class AbstractState(Generic[T_co], Protocol):
    def get(self) -> T_co:
        """Get the current state value."""
        ...

    def watch(self, callback: Callable[[T_co], Any]) -> Callable[[], None]:
        """
        Register a callback to be called when the state changes.

        Returns a function that can be called to unregister the callback.
        """
        ...


class AbstractMutableState(Generic[T], Protocol):
    @property
    def value(self) -> T:
        """The current state value."""
        ...

    def watch(self, callback: Callable[[T], Any]) -> Callable[[], None]:
        """
        Register a callback to be called when the state changes.

        Returns a function that can be called to unregister the callback.
        """
        ...

    def set(self, value: T) -> None:
        """Set the state to a new value."""
        ...

    def update(self, updater: Callable[[T], T]) -> None:
        """
        Update the state using a function that takes the current value and returns a new value.
        """
        ...


def check_state_impl(impl: type[AbstractState]) -> None:
    """
    For type checking purposes only, if the implementation does not match the protocol, this will be flagged by type checkers.
    """


def check_mutable_state_impl(impl: type[AbstractMutableState]) -> None:
    """
    For type checking purposes only, if the implementation does not match the protocol, this will be flagged by type checkers.
    """
