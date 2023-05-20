import pytest

from pydisadm.utils.datetime_utils import convert_to_local_timestamp

@pytest.mark.parametrize(
        'date, expect_timestamp',
        [
            ('2022-05-19 18:17:38', 1652984258),
            ('2023-09-01 16:35:55', 1693586155),
            ('2028-08-12 03:00:00', 1849662000),
        ]
)

def test_convert_to_local_timestamp(date, expect_timestamp):
    timestamp = convert_to_local_timestamp(date)
    assert timestamp == expect_timestamp, 'timestamp dont match expected timestamp'
