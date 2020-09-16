"""The action class."""
from datetime import datetime, date, timedelta
from typing import Callable, Optional

from remind_me_some.event import Event


class Action(Event):
    """The action class."""

    def __init__(
            self,
            name: str,
            due: date,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable[[], None]] = None,
            is_ready_fn: Optional[Callable[[], bool]] = None,
            is_completed_fn: Optional[Callable[[], bool]] = None,
    ) -> None:
        """Initialize an action."""
        super().__init__(
            name=name,
            priority=priority,
            interest_rate=interest_rate,
            callback=callback,
            is_ready_fn=is_ready_fn,
            is_completed_fn=is_completed_fn,
        )
        self.due: date = due

    def __str__(self):
        """Return string information for the current action."""
        return (
            f"{super().__str__()}  =>  "
            f"{self.due} ({'READY' if self.is_ready() else 'NOT READY'})"
        )

    def push_forward(self, days: int = 1) -> None:
        """Bump the due date of the current action and add interest."""
        self.due += timedelta(days=days)
        super().push_forward(days)

    def is_due(self) -> bool:
        """Check if the current action is due."""
        return datetime.now().date() >= self.due
