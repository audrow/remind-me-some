from datetime import date
from freezegun import freeze_time
import pytest

from remind_me_some import Action, schedule_actions


def test_schedule_one_action_per_day():

    a1 = Action("action 1", date(2020, 1, 1), 0.1)
    a2 = Action("action 2", date(2020, 1, 1), 1.5)
    a3 = Action("action 2", date(2020, 1, 1), 2.0)
    actions_ = [a1, a2, a3]

    schedule_actions(actions_, max_actions_per_day=1, is_today_or_after=False)

    assert actions_ == [a3, a2, a1]
    assert a3.due == date(2020, 1, 1)
    assert a2.due == date(2020, 1, 2)
    assert a1.due == date(2020, 1, 3)


def test_schedule_two_actions_per_day():

    a1 = Action("action 1", date(2020, 1, 1), 0.1)
    a2 = Action("action 2", date(2020, 1, 1), 1.5)
    a3 = Action("action 2", date(2020, 1, 1), 2.0)
    actions_ = [a1, a2, a3]

    schedule_actions(actions_, max_actions_per_day=2, is_today_or_after=False)

    assert actions_ == [a3, a2, a1]
    assert a3.due == date(2020, 1, 1)
    assert a2.due == date(2020, 1, 1)
    assert a1.due == date(2020, 1, 2)


def test_schedule_today_or_after():

    a1 = Action("action 1", date(2020, 1, 1), 0.1)
    a2 = Action("action 2", date(2020, 1, 1), 1.5)
    a3 = Action("action 2", date(2020, 1, 1), 2.0)
    actions_ = [a1, a2, a3]

    with freeze_time(date(2020, 2, 1)):

        schedule_actions(actions_, max_actions_per_day=1,
                         is_today_or_after=True)

        assert actions_ == [a3, a2, a1]
        assert a3.due == date(2020, 2, 1)
        assert a2.due == date(2020, 2, 2)
        assert a1.due == date(2020, 2, 3)


def test_excluding_dates():

    def exclude_dates(date_: date):
        return date_ in [date(2020, 1, 1), date(2020, 1, 3)]

    a1 = Action("action 1", date(2020, 1, 1), 0.1)
    a2 = Action("action 2", date(2020, 1, 1), 1.5)
    a3 = Action("action 2", date(2020, 1, 1), 2.0)
    actions_ = [a1, a2, a3]

    schedule_actions(
        actions_,
        max_actions_per_day=1,
        is_today_or_after=False,
        is_exclude_date_fn=exclude_dates,
    )

    assert actions_ == [a3, a2, a1]
    assert a3.due == date(2020, 1, 2)
    assert a2.due == date(2020, 1, 4)
    assert a1.due == date(2020, 1, 5)


@pytest.mark.parametrize('num_actions', [
    -10,
    -1,
    0,
])
def test_invalid_max_actions_per_day(num_actions):
    with pytest.raises(ValueError):
        schedule_actions(
            [],
            max_actions_per_day=num_actions,
        )


@pytest.mark.parametrize('num_days', [
    -10,
    -1,
    0,
])
def test_invalid_days_to_push_forward(num_days):
    with pytest.raises(ValueError):
        schedule_actions(
            [],
            days_to_push_forward=num_days,
        )


@pytest.mark.parametrize('exclude_value', [
    1,
    1.0,
    'hi',
])
def test_invalid_exclude_value(exclude_value):
    with pytest.raises(ValueError):
        schedule_actions(
            [],
            is_exclude_date_fn=exclude_value,
        )
