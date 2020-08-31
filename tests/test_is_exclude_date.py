from datetime import date
import pytest

from remind_me_some import is_exclude_date


@pytest.mark.parametrize("date_, expected", [
    (date(2020, 1, 1), True),
    (date(2020, 7, 4), True),
    (date(2020, 12, 25), True),
    (date(2020, 1, 3), False),
    (date(2020, 7, 5), False),
    (date(2020, 12, 28), False),
])
def test_exclude_holidays(date_, expected):
    assert is_exclude_date(
        date_,
        is_exclude_holidays=True,
        is_exclude_weekends=False,
    ) == expected


@pytest.mark.parametrize("date_, expected", [
    (date(2020, 1, 4), True),
    (date(2020, 1, 5), True),
    (date(2020, 8, 8), True),
    (date(2020, 8, 9), True),
    (date(2020, 1, 3), False),
    (date(2020, 1, 6), False),
    (date(2020, 8, 7), False),
    (date(2020, 8, 10), False),
])
def test_exclude_weekends(date_, expected):
    assert is_exclude_date(
        date_,
        is_exclude_holidays=False,
        is_exclude_weekends=True,
    ) == expected


@pytest.mark.parametrize("date_, expected", [
    (date(2020, 1, 3), True),
    (date(2020, 8, 7), True),
    (date(2020, 1, 2), False),
    (date(2020, 1, 4), False),
    (date(2020, 8, 6), False),
    (date(2020, 8, 8), False),
])
def test_exclude_fridays(date_, expected):
    assert is_exclude_date(
        date_,
        is_exclude_holidays=False,
        is_exclude_weekends=False,
        is_exclude_friday=True,
    ) == expected


@pytest.mark.parametrize("date_, expected", [
    (date(2020, 1, 1), True),
    (date(2020, 7, 4), True),
    (date(2020, 12, 25), True),
    (date(2020, 12, 28), False),
    (date(2020, 1, 4), True),
    (date(2020, 1, 5), True),
    (date(2020, 8, 8), True),
    (date(2020, 8, 9), True),
    (date(2020, 1, 3), True),
    (date(2020, 8, 7), True),
    (date(2020, 1, 2), False),
    (date(2020, 1, 6), False),
    (date(2020, 8, 10), False),
])
def test_exclude_holidays_fridays_and_weekends(date_, expected):
    assert is_exclude_date(
        date_,
        is_exclude_holidays=True,
        is_exclude_weekends=True,
        is_exclude_friday=True,
    ) == expected
