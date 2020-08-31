from datetime import date
from freezegun import freeze_time
import pytest

from remind_me_some import Action


@pytest.mark.parametrize('daily_interest, num_days', [
    (0, 1),
    (0, 100),
    (0.05, 1),
    (0.05, 10),
    (1.00, 1),
    (1.00, 10),
])
def test_push_forward(daily_interest, num_days):
    priority = 1
    action = Action(
        name='name',
        due=date(2020, 1, 1),
        priority=priority,
        daily_interest_rate=daily_interest,
    )
    action.push_forward(num_days)
    assert action.priority == (1 + daily_interest)**num_days


@pytest.mark.parametrize('priority', [
    -10,
    -1,
    -0.1,
    0,
])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        Action(
            name='name',
            due=date(2020, 1, 1),
            priority=priority,
            daily_interest_rate=1.0,
        )


@pytest.mark.parametrize('interest_rate', [
    -10,
    -1,
    -0.1,
])
def test_invalid_interest_rate(interest_rate):
    with pytest.raises(ValueError):
        Action(
            name='name',
            due=date(2020, 1, 1),
            priority=1.0,
            daily_interest_rate=interest_rate,
        )


def test_str_fn():
    action = Action(
        name='name',
        due=date(2020, 1, 1),
        priority=1.0,
        daily_interest_rate=1.0,
    )
    assert type(action.__str__()) is str


def test_default_fns():
    action = Action(
        name='name',
        due=date(2020, 1, 2),
        priority=1.0,
        daily_interest_rate=1.0,
    )
    with freeze_time(date(2020, 1, 1)):
        assert not action.is_ready()
        with pytest.raises(RuntimeError):
            action.callback()
        assert not action.is_completed()
    with freeze_time(date(2020, 1, 3)):
        assert action.is_ready()
        assert not action.is_completed()
        for _ in range(5):
            action.callback()
            assert action.is_completed()
