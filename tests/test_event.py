import pytest

from remind_me_some.event import Event


@pytest.mark.parametrize('interest, steps', [
    (0, 1),
    (0, 100),
    (0.05, 1),
    (0.05, 10),
    (1.00, 1),
    (1.00, 10),
])
def test_push_forward(interest, steps):
    priority = 1
    action = Event(
        name='name',
        priority=priority,
        interest_rate=interest,
    )
    action.push_forward(steps)
    assert action.priority == (1 + interest) ** steps


@pytest.mark.parametrize('steps', [
    -100,
    -1,
    0
])
def test_invalid_push_forward(steps):
    priority = 1
    action = Event(
        name='name',
        priority=priority,
        interest_rate=1,
    )
    with pytest.raises(ValueError):
        action.push_forward(steps)


@pytest.mark.parametrize('priority', [
    -10,
    -1,
    -0.1,
    0,
])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        Event(
            name='name',
            priority=priority,
            interest_rate=1.0,
        )


@pytest.mark.parametrize('interest_rate', [
    -10,
    -1,
    -0.1,
])
def test_invalid_interest_rate(interest_rate):
    with pytest.raises(ValueError):
        Event(
            name='name',
            priority=1.0,
            interest_rate=interest_rate,
        )


def test_str_fn():
    event = Event(
        name='name',
        priority=1.0,
        interest_rate=1.0,
    )
    assert type(event.__str__()) is str


def test_default_fns():
    event = Event(
        name='name',
        priority=1.0,
        interest_rate=1.0,
    )
    assert event.is_ready()
    assert not event.is_completed()
    event.callback()
    assert not event.is_ready()
    assert event.is_completed()

    with pytest.raises(RuntimeError):
        event.callback()
    assert not event.is_ready()
    assert event.is_completed()


def test_try_run():

    def no_arg_fn():
        pass

    def one_arg_fn(_):
        pass

    def two_args_fn(_, __):
        pass

    event = Event(
        name='name',
        priority=1.0,
        interest_rate=1.0,
    )

    event._try_run_args(no_arg_fn)
    event._try_run_args(one_arg_fn)
    with pytest.raises(TypeError):
        event._try_run_args(two_args_fn)
