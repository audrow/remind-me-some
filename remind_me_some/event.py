"""The event class."""

import logging
from typing import Any, Callable, Optional


logger = logging.getLogger(__name__)


class Event:
    """The event class."""

    def __init__(
            self,
            name: str,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable[[], None]] = None,
            is_ready_fn: Optional[Callable[[], bool]] = None,
            is_completed_fn: Optional[Callable[[], bool]] = None,
    ) -> None:
        """Initialize an event."""
        if priority <= 0:
            raise ValueError("Priority must be a positive number")
        if interest_rate < 0:
            raise ValueError("Interest should be a non-negative number")
        if is_ready_fn is None:
            is_ready_fn = self.is_due
        if is_completed_fn is None:
            is_completed_fn = self.is_called
        self.name: str = name
        self.priority: float = priority
        self._interest_rate: float = interest_rate
        self._callback: Optional[Callable] = callback
        self._is_ready_fn: Callable = is_ready_fn
        self._is_completed_fn: Callable = is_completed_fn

        self._callback_count: int = 0

    def __str__(self) -> str:
        """Get a string with details of the current event."""
        return f"{self.name:<15} (priority={self.priority:.2f})"

    def __eq__(self, other):
        """Check if two events are the same by comparing their names."""
        return self.name == other.name

    def push_forward(self, steps: int = 1) -> None:
        """Increase the priority of event by applying interest."""
        logger.debug(f"Push forward '{self.name}' by {steps} steps")
        if steps < 1:
            raise ValueError('Must push forward a positive number of steps')
        self.priority *= (1 + self._interest_rate) ** steps

    def is_due(self) -> bool:
        """Check if the event is due."""
        return not self.is_completed()

    def is_called(self) -> bool:
        """Check if the event has been called."""
        return self._callback_count > 0

    def callback(self) -> Any:
        """Call the event's callback."""
        logger.debug(f"Call callback for '{self.name}'")
        if self.is_ready():
            self._callback_count += 1
            if callable(self._callback):
                return self._try_run_args(self._callback)
        else:
            raise RuntimeError(
                f"Callback '{self.name}' called before it's ready")

    def is_ready(self) -> bool:
        """Check if an event is ready."""
        return (
            self._try_run_args(self._is_ready_fn)
            and not self.is_completed()
        )

    def is_completed(self) -> bool:
        """Check if an event has been completed."""
        return self._try_run_args(self._is_completed_fn)

    def _try_run_args(self, fn) -> Any:
        try:
            return fn()
        except TypeError:
            pass
        try:
            return fn(self)
        except TypeError:
            pass

        raise TypeError("Function could not be run")
