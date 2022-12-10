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
import numpy as np


# example constant variable
NAME = "nonlinearequations"

def solve_seidel(a: List[List[float]], v: List[float]) -> List[float]:
    
    def get_column(a, i):
        return [row[i] for row in a]

    eps = 0.01
    max_iterations = 1000
    n = len(a)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            matrix[i][j] = a[i][j]

    b = get_column(a, n-1)
    x = np.zeros_like(b, dtype=np.double)

    for k in range(max_iterations):
        
        x_old  = x.copy()
        
        for i in range(len(matrix)):
            x[i] = (b[i] - np.dot(matrix[i][:i], x[:i]) - np.dot(matrix[i][(i+1):], x_old[(i+1):])) / matrix[i][i]
            
        if np.linalg.norm(x - x_old, ord=np.inf) / np.linalg.norm(x, ord=np.inf) < eps:
            break
            
    return x


def solve_simple_iterations(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_newton(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError
