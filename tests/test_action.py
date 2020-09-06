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
        interest_rate=daily_interest,
    )
    action.push_forward(num_days)
    assert action.priority == (1 + daily_interest)**num_days


@pytest.mark.parametrize('check_date', [
    date(2020, 1, 2),
    date(2020, 1, 3),
    date(2020, 2, 1),
    date(2021, 1, 1),
])
def test_default_fns(check_date):
    action = Action(
        name='name',
        due=date(2020, 1, 2),
        priority=1.0,
        interest_rate=1.0,
    )
    with freeze_time(date(2020, 1, 1)):
        assert not action.is_ready()
        with pytest.raises(RuntimeError):
            action.callback()
        assert not action.is_completed()
    with freeze_time(check_date):
        assert action.is_ready()
        assert not action.is_completed()
        action.callback()
        assert not action.is_ready()
        assert action.is_completed()
