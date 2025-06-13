from typing import Any, Callable, Generic, Protocol, TypeVar, runtime_checkable

T = TypeVar("T")
U = TypeVar("U")
T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class AbstractState(Generic[T_co], Protocol):
    def watch(self, callback: Callable[[T_co], Any]) -> Callable[[], None]:
        """
        Register a callback to be called when the state changes.

        Returns a function that can be called to unregister the callback.
        """
        ...

    def map(self, mapper: Callable[[T_co], U], /) -> "AbstractState[U]":
        """
        Create a new derived state that transforms this state's value using the provided mapper function.

        The derived state will automatically update when the original state changes.

        The derived state is immutable, meaning you cannot set its value directly.
        """
        ...

    def bind(self, target: Any, property_name: str) -> Any:
        """
        Bind this state's value to a property on a target object.

        When the state changes, the target object's property will be updated automatically.
        Returns a binding object that can be used to manage the binding.
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

    def map(self, mapper: Callable[[T], U], /) -> "AbstractState[U]":
        """
        Create a new derived state that transforms this state's value using the provided mapper function.

        The derived state will automatically update when the original state changes.

        The derived state is immutable, meaning you cannot set its value directly.
        """
        ...

    def bind(self, target: Any, property_name: str) -> Any:
        """
        Bind this state's value to a property on a target object.

        When the state changes, the target object's property will be updated automatically.
        Returns a binding object that can be used to manage the binding.
        """
        ...

    def bind_twoway(self, target: Any, property_name: str) -> Any:
        """
        Create a bidirectional binding between this state and a property on a target object.

        Changes to either the state or the target property will be synchronized automatically.
        Returns a binding object that can be used to manage the binding.
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
