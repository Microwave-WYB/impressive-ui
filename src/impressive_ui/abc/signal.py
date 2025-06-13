from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

T = TypeVar("T")


class AbstractSignal(Generic[T], ABC):
    @abstractmethod
    def emit(self, value: T) -> None:
        """Emit a new value to the signal."""
        ...

    @abstractmethod
    def subscribe(self, callback: Callable[[T], None]) -> None:
        """Subscribe to the signal with a callback that receives emitted values."""
        ...
