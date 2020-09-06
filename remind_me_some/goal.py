from datetime import datetime, date, timedelta
from typing import Callable, Optional

from remind_me_some.event import Event
from remind_me_some.action import Action


class Goal(Event):

    def __init__(
            self,
            name: str,
            frequency: timedelta,
            priority: float = 1.0,
            interest_rate: float = 0.05,
            last_completed: Optional[date] = None,
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
        self._frequency = frequency
        self._last_completed = last_completed

    def make_action(self) -> Action:
        if self._last_completed is not None:
            due = self._last_completed + self._frequency
        else:
            due = datetime.now().date()

        return Action(
            name=self.name,
            due=due,
            priority=self.priority,
            interest_rate=self._interest_rate,
            callback=self._callback,
            is_ready_fn=Action.is_due,
            is_completed_fn=Action.is_called,
        )

    def mark_as_completed(self) -> None:
        self._last_completed = datetime.now().date()

    @property
    def last_completed(self) -> date:
        return self._last_completed
