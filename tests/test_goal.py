from datetime import date, datetime, timedelta
from freezegun import freeze_time

from remind_me_some import Goal


def test_make_action_no_last_date():
    goal = Goal('name', timedelta(days=3))
    action = goal.make_action()
    assert action.is_ready()
    assert not action.is_completed()
    action.callback()
    assert not action.is_ready()
    assert action.is_completed()


def test_make_action_with_last_date():

    goal = Goal(
        'name',
        timedelta(days=3),
        last_completed=date(2020, 1, 1),
    )
    action = goal.make_action()
    with freeze_time(date(2020, 1, 3)):
        assert not action.is_ready()
        assert not action.is_completed()
    with freeze_time(date(2020, 1, 4)):
        assert action.is_ready()
        assert not action.is_completed()
        action.callback()
        assert not action.is_ready()
        assert action.is_completed()


def test_mark_as_completed():
    goal = Goal(
        'name',
        timedelta(days=3),
    )
    assert goal.last_completed is None
    date1 = date(2020, 1, 1)
    with freeze_time(date1):
        goal.mark_as_completed()
    assert goal.last_completed == date1

    date2 = date(2020, 1, 2)
    with freeze_time(date2):
        goal.mark_as_completed()
    assert goal.last_completed == date2
