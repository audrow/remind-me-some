from typing import Callable, Optional


class Event:

    def __init__(
            self,
            name: str,
            priority: float,
            interest_rate: float,
            callback: Optional[Callable] = None,
            is_ready_fn: Optional[Callable] = None,
            is_completed_fn: Optional[Callable] = None,
    ) -> None:
        if priority <= 0:
            raise ValueError("Priority must be a positive number")
        if interest_rate < 0:
            raise ValueError("Interest should be a non-negative number")
        if is_ready_fn is None:
            is_ready_fn = self._default_is_ready_fn
        if is_completed_fn is None:
            is_completed_fn = self._default_is_completed_fn
        self.name: str = name
        self.priority: float = priority
        self._interest_rate: float = interest_rate
        self._callback: Optional[Callable] = callback
        self._is_ready_fn: Callable = is_ready_fn
        self._is_completed_fn: Callable = is_completed_fn

        self._callback_count: int = 0

    def __str__(self) -> str:
        return f"(priority={self.priority:.2f})\t{self.name}"

    def push_forward(self, steps: int = 1) -> None:
        if steps < 1:
            raise ValueError('Must push forward a positive number of steps')
        self.priority *= (1 + self._interest_rate) ** steps

    def _default_is_ready_fn(self):
        return not self.is_completed()

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
