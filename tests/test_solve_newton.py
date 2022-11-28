import math

import pytest

from nonlinearequations.base import solve_newton
from scipy.optimize import fsolve


# Пример системы с двумя неизвестными
def system_two_variables(p):
    x, y = p
    return (x + y ** 2 - 4, math.exp(x) + x * y - 3)


def system_three_variables(p):
    x, y, z = p
    return (2*x - z/x, math.exp(y) + x * y, x + y*z + z/2)

def system_three_variables_2(p):
    x, y, z = p
    return (x**2+y**2+z**2-1, 2*x**2+y**2-4*z, 3*x**2-4*y+z**2)

def test_two_variables():
    eps = 10e-6
    (x_expected, y_expected) = fsolve(system_two_variables, (1, 1), epsfcn=eps)
    x_actual, y_actual = solve_newton(system_two_variables,[1,1] ,eps)


    assert x_expected == pytest.approx(x_actual, eps)
    assert y_expected == pytest.approx(y_actual, eps)


def test_three_variables():
    eps = 10e-6
    (x_expected, y_expected, z_expected) = fsolve(system_three_variables, (1, 1, 1), epsfcn=eps)
    x_actual, y_actual, z_actual = solve_newton(system_three_variables,[1,1,1], eps)


    assert x_expected == pytest.approx(x_actual, eps)
    assert y_expected == pytest.approx(y_actual, eps)
    assert z_expected == pytest.approx(z_actual, eps)


def test_three_variables_2():
    eps = 0.005
    (x_expected, y_expected, z_expected) = fsolve(system_three_variables_2, (0.5, 0.5, 0.5), epsfcn=eps)
    x_actual, y_actual, z_actual = solve_newton(system_three_variables_2,[0.5,0.5,0.5], eps)

    assert x_expected == pytest.approx(x_actual, eps)
    assert y_expected == pytest.approx(y_actual, eps)
    assert z_expected == pytest.approx(z_actual, eps)