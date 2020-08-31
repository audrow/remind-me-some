from datetime import datetime, date, timedelta
from typing import Callable, Optional


class Action:

    def __init__(
            self,
            name: str,
            due: date,
            priority: float,
            daily_interest_rate: float = 0.05,
            callback: Optional[Callable] = None,
            is_ready_fn: Optional[Callable] = None,
            is_completed_fn: Optional[Callable] = None,
    ) -> None:
        if priority <= 0:
            raise ValueError("Priority must be a positive number")
        if daily_interest_rate < 0:
            raise ValueError("Daily interest should be a non-negative number")
        if is_ready_fn is None:
            is_ready_fn = self._default_is_ready_fn
        if is_completed_fn is None:
            is_completed_fn = self._default_is_completed_fn
        self.name: str = name
        self.due: date = due
        self.priority: float = priority
        self._daily_interest_rate: float = daily_interest_rate
        self._callback: Optional[Callable] = callback
        self._is_ready_fn: Callable = is_ready_fn
        self._is_completed_fn: Callable = is_completed_fn

        self._callback_count: int = 0

    def __str__(self) -> str:
        return f"(priority={self.priority:.2f})\t{self.name}:\t{self.due}"

    def push_forward(self, days: int = 1) -> None:
        self.due += timedelta(days=days)
        self.priority *= (1 + self._daily_interest_rate) ** days

    def _default_is_ready_fn(self):
        return self.due < datetime.now().date()

    def _default_is_completed_fn(self):
        return self._callback_count > 0

    def callback(self):
        if self.is_ready():
            self._callback_count += 1
            if callable(self._callback):
                return self._callback()
        else:
            raise RuntimeError(
                f"Callback '{self.name}' called before it's ready")

    def is_ready(self):
        return self._is_ready_fn()

    def is_completed(self):
        return self._is_completed_fn()
