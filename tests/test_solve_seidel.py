import pytest

from nonlinearequations.base import solve_seidel


def test_raises_error():
    with pytest.raises(NotImplementedError):
        solve_seidel([[]], [])
