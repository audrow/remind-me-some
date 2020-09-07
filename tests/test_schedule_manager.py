from datetime import date, timedelta
from freezegun import freeze_time
import pytest

from remind_me_some.schedule_manager import ScheduleManager
from remind_me_some.goal import Goal


@pytest.fixture
def goals_and_mocks(mocker):
    callback_mock_1 = mocker.Mock()
    callback_mock_2 = mocker.Mock()
    callback_mock_3 = mocker.Mock()
    goal_1 = Goal('goal 1', timedelta(days=10),
                  priority=2.5, callback=callback_mock_1)
    goal_2 = Goal('goal 2', timedelta(days=3),
                  priority=1.5, callback=callback_mock_2)
    goal_3 = Goal('goal 3', timedelta(weeks=2),
                  priority=1.2, callback=callback_mock_3)
    return [
        (goal_1, goal_2, goal_3),
        (callback_mock_1, callback_mock_2, callback_mock_3)
    ]


@pytest.fixture
def schedule_manager_and_mocks(goals_and_mocks):
    goals = goals_and_mocks[0]
    mocks = goals_and_mocks[1]

    sm = ScheduleManager()
    sm.add_goals(*goals)
    return sm, mocks


def test_program_flow(goals_and_mocks):
    goals = goals_and_mocks[0]
    mock_1, mock_2, mock_3 = goals_and_mocks[1]

    sm = ScheduleManager()
    assert not sm.goals
    assert not sm.actions

    sm.add_goals(*goals)
    assert len(sm.goals) == 3
    assert not sm.actions

    with freeze_time(date(2020, 1, 1)):
        sm.update_schedule()
    assert len(sm.goals) == 3
    assert len(sm.actions) == 3
    assert not mock_1.called
    assert not mock_2.called
    assert not mock_3.called

    # holiday so nothing happens
    with freeze_time(date(2020, 1, 1)):  # holiday
        sm.run()
    assert not mock_1.called
    assert not mock_2.called
    assert not mock_3.called

    # call the callback for goal 1
    with freeze_time(date(2020, 1, 2)):  # tuesday
        sm.run()
    assert mock_1.call_count == 1
    assert not mock_2.called
    assert not mock_3.called
    assert len(sm.actions) == 3

    # running run several times doesn't run the callback again
    for _ in range(5):
        with freeze_time(date(2020, 1, 2)):  # tuesday
            sm.run()
        assert mock_1.call_count == 1
        assert not mock_2.called
        assert not mock_3.called
        assert len(sm.actions) == 2

    # nothing happens on the weekend
    with freeze_time(date(2020, 1, 4)):  # saturday
        sm.update_schedule()
        sm.run()
    assert mock_1.call_count == 1
    assert not mock_2.called
    assert not mock_3.called
    assert len(sm.actions) == 3

    # updating creates a new first goal
    with freeze_time(date(2020, 1, 6)):  # monday
        sm.update_schedule()
    assert len(sm.goals) == 3
    assert len(sm.actions) == 3
    assert mock_1.call_count == 1
    assert not mock_2.called
    assert not mock_3.called

    # second goal is ready
    for _ in range(5):
        with freeze_time(date(2020, 1, 6)):  # monday
            sm.run()
            sm.run()
        assert mock_1.call_count == 1
        assert mock_2.call_count == 1
        assert not mock_3.called
        assert len(sm.actions) == 2

    # third goal is ready
    for _ in range(5):
        with freeze_time(date(2020, 1, 7)):  # tuesday
            sm.update_schedule()
            sm.run()
        assert mock_1.call_count == 1
        assert mock_2.call_count == 1
        assert mock_3.call_count == 1

    # nothing is ready this day
    with freeze_time(date(2020, 1, 8)):  # wednesday
        sm.update_schedule()
        sm.run()
    assert mock_1.call_count == 1
    assert mock_2.call_count == 1
    assert mock_3.call_count == 1

    # Second goal is ready
    with freeze_time(date(2020, 1, 10)):  # wednesday
        sm.update_schedule()
        sm.run()
    assert mock_1.call_count == 1
    assert mock_2.call_count == 2
    assert mock_3.call_count == 1


def test_string_methods(goals_and_mocks):
    sm = ScheduleManager()
    str1 = str(sm)
    sm.add_goals(*goals_and_mocks[0])
    str2 = str(sm)
    sm.update_schedule()
    str3 = str(sm)
    assert str1 != str2
    assert str2 != str3
    assert str3 != str1


def test_get_invalid_goal(schedule_manager_and_mocks):
    sm = schedule_manager_and_mocks[0]
    with pytest.raises(ValueError):
        sm._get_goal('foo')
