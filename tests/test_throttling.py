from datetime import timedelta
from time import sleep

from pytest import mark

from app.helper.throttling import RateLimit, gcraMemory


@mark.parametrize(
    "requests, delta, limit, expected",
    [
        (6, 1, 5, True),
        (2, 1, 1, True),
        (6, 10, 5, True),
        (1, 1, 1, False),
        (4, 10, 5, False),
        (5, 10, 5, False)
    ]
)
def test_rate_limit(requests, delta, limit, expected):
    gcra = gcraMemory()
    rate_limit = RateLimit(limit, period=1*1000)
    for _ in range(requests):
        rejected = gcra.update('key', rate_limit)
        # breakpoint()
        if rejected:
            break
        sleep(delta/requests)
    assert rejected == expected
