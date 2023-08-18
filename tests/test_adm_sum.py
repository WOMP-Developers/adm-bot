import pytest
from pydisadm.utils.adm_utils import adm_from_index

@pytest.mark.parametrize(
        'military, industrial, strategic, adm',
        [
            (0, 0, 0, 1),
            (1, 0, 0, 1.6),
            (4, 0, 4, 4.0),
            (5, 5, 5, 6.0),
            (5, 2, 1, 5.1)
        ]
)

def test_adm_sum(military, industrial, strategic, adm):
    assert adm_from_index(military, industrial, strategic) == adm
