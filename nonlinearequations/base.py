"""
nonlinearequations base module.

This is the principal module of the nonlinearequations project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
import pprint
from typing import List


# example constant variable
NAME = "nonlinearequations"


def solve_seidel(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_simple_iterations(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_newton(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def derivative(equation, pt, variable, j):
    delta = pt[variable]/10e9 if (pt[variable] is not 0) else 1/10e9
    diff = (equation(pt[:variable] + [pt[variable] + delta] + pt[variable+1:])[j] - equation(pt)[j]) / delta
    return diff


def matrix_output(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')
        print()


def jacobi(system, point):
    dimention = len(system(point))
    jacobi_matrix = [[0 for j in range(dimention)] for i in range(dimention)]
    for i in range(dimention):
        for j in range(dimention):
            jacobi_matrix[j][i] = derivative(system, point, i, j)
    return jacobi_matrix