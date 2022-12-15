"""
nonlinearequations base module.

"""
import copy
from typing import List

NAME = "nonlinearequations"


def solve_newton(systems, x0, eps=0.00001) -> List[float]:
    def stop_condition_newton(delta_x):
        """
        Функция для проверки условия прекращения алгоритма в методе Ньютона
        """
        max = abs(delta_x[0][0])
        for i in range(len(delta_x)):
            if abs(delta_x[i][0]) > max:
                max = abs(delta_x[i][0])
        return max

    k = 0
    # считаем матрицу якоби подставив значение из x0 (matrixa)
    matrix = __jacobi(systems, x0)

    # для деления F на матрицу якоби нужно найти обратную матрицу
    obratnay_matrix = __get_matrix_inverse(matrix)

    # найдем вектор F подставив в исходную систему значения x0 и домножим полученный вектор на -1
    # тк мы решили полставлять в систему кортеж, то преобразуем вектор в кортеж, а после подстановки вернем все как было

    F = list(systems(x0))
    F = __get_matrix_minus(list(map(lambda x: [x], F)))


    # ищем delta_x0 = obratnay_matrixa * F
    delta_x0 = __get_matrix_mult(obratnay_matrix, F)

    # ищем x1 = x0 + delta_x0
    k += 1
    x1 = __get_matrix_sum(list(map(lambda x: [x], x0)), delta_x0)
    x1 = list(map(lambda x: x[0], x1))

    # далее повторяем те же дейсвия в цикле
    while stop_condition_newton(delta_x0) > eps:
        matrix = __jacobi(systems, x1)
        obratnay_matrix = __get_matrix_inverse(matrix)

        F = list(systems(x1))
        F = __get_matrix_minus(list(map(lambda x: [x], F)))

        delta_x0 = __get_matrix_mult(obratnay_matrix, F)

        k += 1
        x0 = x1
        x1 = __get_matrix_sum(list(map(lambda x: [x], x0)), delta_x0)
        x1 = list(map(lambda x: x[0], x1))

    return x1


def __get_matrix_transpose(m):
    """
    Функция вовзвращает транспонированную матрицу
    """
    a = list(zip(*m))
    for i in range(len(a)):
        a[i] = list(a[i])
    return a



def __get_matrix_minor(m, i, j):
    """
    Функция вовзращает минор матрицы
    """
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]



def __get_matrix_determinant(m):
    """
    Функция для расчета определителя
    """
    # для матрицы 2 на 2
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * __get_matrix_determinant(__get_matrix_minor(m, 0, c))
    return determinant



def __get_matrix_inverse(m):
    """
    Функция возвращает обратную матрицу
    """
    determinant = __get_matrix_determinant(m)
    if determinant == 0:
        pass
    # если матрица 2 на 2
    if len(m) == 2:
        return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                [-1 * m[1][0] / determinant, m[0][0] / determinant]]
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = __get_matrix_minor(m, r, c)
            cofactorRow.append(((-1) ** (r + c)) * __get_matrix_determinant(minor))
        cofactors.append(cofactorRow)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c] / determinant
    return __get_matrix_transpose(cofactors)


def __get_matrix_mult(A, b):
    """
    Функция для умножения матриц
    """
    s = 0  # сумма
    t = []  # временная матрица
    m3 = []  # конечная матрица
    if len(b) != len(A[0]):
        raise Exception("Матрицы не могут быть перемножены, не соответсвие размеров")
    else:

        for z in range(0, len(A)):
            for j in range(0, len(b[0])):
                for i in range(0, len(A[0])):
                    s = s + A[z][i] * b[i][j]
                t.append(s)
                s = 0
            m3.append(t)
            t = []
    return m3


def __get_matrix_minus(a):
    """
    Функция вовращает матрицу умноженную на -1
    """
    b = copy.deepcopy(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            b[i][j] *= -1
    return b



def __get_matrix_sum(a, b):
    """
    Функция возвращает сумму матриц
    """
    if (len(a) != len(b)) or (len(a[0]) != len(b[0])):
        raise Exception("Матрицы нельзя сложить, не соотвествие размеров")
    s = copy.deepcopy(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            s[i][j] += b[i][j]
    return s


def __derivative(equation, pt, variable, j):
    delta = pt[variable] / 10e6 if (pt[variable] is not 0) else 1 / 10e6
    diff = (equation(pt[:variable] + [pt[variable] + delta] + pt[variable + 1:])[j] - equation(pt)[j]) / delta
    return diff


def __matrix_output(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')
        print()


def __jacobi(system, point):
    dimention = len(system(point))
    jacobi_matrix = [[0 for j in range(dimention)] for i in range(dimention)]
    for i in range(dimention):
        for j in range(dimention):
            jacobi_matrix[j][i] = __derivative(system, point, i, j)
    return jacobi_matrix
