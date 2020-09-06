from datetime import datetime, date, timedelta
from typing import Callable, Optional
from .event import Event


class Action(Event):

    def __init__(
            self,
            name: str,
            due: date,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable] = None,
            is_ready_fn: Optional[Callable] = None,
            is_completed_fn: Optional[Callable] = None,
    ) -> None:
        super().__init__(
            name=name,
            priority=priority,
            interest_rate=interest_rate,
            callback=callback,
            is_ready_fn=is_ready_fn,
            is_completed_fn=is_completed_fn,
        )
        self.due: date = due

    def push_forward(self, days: int = 1) -> None:
        self.due += timedelta(days=days)
        super().push_forward(days)

    def _default_is_ready_fn(self):
        return self.due < datetime.now().date()
