from datetime import date
import logging
from typing import Callable, List

from remind_me_some.action import Action
from remind_me_some.goal import Goal
from remind_me_some.schedule_actions import schedule_actions
from remind_me_some.is_exclude_date import is_exclude_date


logger = logging.getLogger(__name__)


class ScheduleManager:

    def __init__(
            self,
            max_actions_per_day: int = 1,
            is_exclude_date_fn: Callable[[date], bool] = is_exclude_date,
    ):
        self._max_actions_per_day = max_actions_per_day
        self._is_exclude_date_fn = is_exclude_date_fn

        self._goals: List[Goal] = []
        self._actions: List[Action] = []

    def __str__(self):
        out = ""
        if self._actions:
            contents = self._actions
            out += "Actions:\n========\n"
        elif self._goals:
            contents = self._goals
            out += "Goals:\n======\n"
        else:
            return f'<Empty {self.__class__.__name__}>'
        for a in contents:
            out += f'{a}\n'
        return out

    @property
    def actions(self) -> List[Action]:
        return self._actions

    @property
    def goals(self) -> List[Goal]:
        return self._goals

    def add_goal(self, goal: Goal):
        logger.debug(f"Goal '{goal.name}' added")
        if goal not in self._goals:
            self._goals.append(goal)

    def add_goals(self, *goals: Goal):
        for g in goals:
            self.add_goal(g)

    def run(self):
        action = self._actions[0]
        if action.is_ready():
            logger.debug(f"Action '{action.name}' is ready")
            logger.info(f"Run callback for action '{action.name}'")
            action.callback()
        elif action.is_completed():
            logger.debug(f"Action '{action.name}' is completed")
            goal = self._get_goal(action.name)
            goal.mark_as_completed()
            logger.info(f"Remove action completed '{action.name}'")
            self._actions.remove(action)

    def _get_goal(self, name: str) -> Goal:
        for g in self._goals:
            if g.name == name:
                return g
        raise ValueError(f"No goal '{name}' found")

    def update_schedule(self):
        self._update_actions()
        schedule_actions(
            self._actions,
            max_actions_per_day=self._max_actions_per_day,
            is_exclude_date_fn=self._is_exclude_date_fn,
        )

    def _update_actions(self):
        for goal in self._goals:
            if goal not in self._actions:
                logger.info(f"Creat action for goal '{goal.name}'")
                self._actions.append(
                    goal.make_action()
                )