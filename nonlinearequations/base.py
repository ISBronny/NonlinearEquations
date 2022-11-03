"""
nonlinearequations base module.

This is the principal module of the nonlinearequations project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
from typing import List


# example constant variable
NAME = "nonlinearequations"


def solve_seidel(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_simple_iterations(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_newton(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError
