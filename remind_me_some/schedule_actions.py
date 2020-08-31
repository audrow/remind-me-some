from datetime import datetime, date
from typing import Any, Callable, Optional, List

from remind_me_some.action import Action


def schedule_actions(
        actions,
        max_actions_per_day: int = 1,
        days_to_push_forward: int = 1,
        is_today_or_after: bool = True,
        is_exclude_date_fn: Optional[Callable] = None,
) -> None:

    def _return_false(_: Any):
        return False

    def _sort_actions(_actions: List[Action]):
        _actions.sort(key=lambda a: (a.due, -a.priority))

    if max_actions_per_day <= 0:
        raise ValueError("Must have a positive max number of actions per day")
    if days_to_push_forward <= 0:
        raise ValueError(
            "Must have a positive number of days to reschedule actions")
    if is_exclude_date_fn is None:
        is_exclude_date_fn = _return_false
    elif not callable(is_exclude_date_fn):
        raise ValueError("Exclude date function must be callable")

    _sort_actions(actions)

    last_date: Optional[date] = None
    num_at_last_date: Optional[int] = None
    idx = 0
    while idx < len(actions):
        action = actions[idx]

        if (is_today_or_after and action.due < datetime.now().date()) \
                or is_exclude_date_fn(action.due):
            action.push_forward(days_to_push_forward)
            _sort_actions(actions)
            continue

        if action.due == last_date:
            if num_at_last_date < max_actions_per_day:
                num_at_last_date += 1
                idx += 1
            else:
                action.push_forward(days_to_push_forward)
                _sort_actions(actions)
        else:
            last_date = action.due
            num_at_last_date = 1
            idx += 1
