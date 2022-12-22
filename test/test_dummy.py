"""Template test module."""
import pytest

# import the internal libs and test
from amiga_pkg import math


class TestDummy:
    """Template test class."""
    @pytest.mark.parametrize("a,b,c", [(1,2,3), (2,3,5)])
    def test_add(self, a, b, c) -> None:
        expected = math.add(a, b)
        assert expected == c
