"""Template test module."""
import pytest

# import the internal libs and test
from amiga_package import ops, __version__


class TestDummy:
    """Template test class."""
    def test_smoke(self) -> None:
        assert __version__ == "0.0.1"

    @pytest.mark.parametrize("a,b,c", [(1,2,3), (2,3,5)])
    def test_add(self, a, b, c) -> None:
        expected = ops.add(a, b)
        assert expected == c
