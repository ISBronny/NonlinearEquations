import pytest

from nonlinearequations.base import solve_simple_iterations


def test_raises_error():
    with pytest.raises(NotImplementedError):
        solve_simple_iterations([[]], [])
