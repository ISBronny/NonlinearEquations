import pytest

from nonlinearequations.base import solve_newton


def test_raises_error():
    with pytest.raises(NotImplementedError):
        solve_newton([[]], [])
