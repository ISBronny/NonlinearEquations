"""
nonlinearequations base module.

This is the principal module of the nonlinearequations project.
here you put your main classes and objects.

Be creative! do whatever you want!

If you want to replace this with a Flask application run:

    $ make init

and then choose `flask` as template.
"""
import copy
from typing import List


# example constant variable
NAME = "nonlinearequations"


def solve_seidel(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError


def solve_simple_iterations(a: List[List[float]], v: List[float]) -> List[float]:
    raise NotImplementedError

# функция вовзвращает транспонированную матрицу
def transposeMatrix(m):
    a = list(zip(*m))
    for i in range(len(a)):
        a[i] = list(a[i])
    return a

# функция вовзращает минор матрицы
def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

# функция для расчета определителя
def getMatrixDeternminant(m):
    # для матрицы 2 на 2
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

# функция возвращает обратную матрицу
def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    if determinant == 0:
        pass
    # если матрица 2 на 2
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c]= cofactors[r][c]/determinant
    return cofactors

def MatrixIkobi(systems, x):
    # тут записан просто пример выходных данных
    return [[1, 1], [2*x[0][0],2*x[1][0]]]


# функция для умножения матриц
def getMatrixMult(A,b):
    s=0     #сумма
    t=[]    #временная матрица
    m3=[] # конечная матрица
    if len(b)!=len(A[0]):
        print ("Матрицы не могут быть перемножены")
    else:

        for z in range(0,len(A)):
            for j in range(0,len(b[0])):
                for i in range(0,len(A[0])):
                   s=s+A[z][i]*b[i][j]
                t.append(s)
                s=0
            m3.append(t)
            t=[]
    return m3

# функция вовращает матрицу умноженную на -1
def getMatrixMult_to_1(a):
    b=copy.deepcopy(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            b[i][j]*=-1
    return b

# функция меняет кортеж на вектор
def tuple_to_vector(p):
    a=[]
    for val in p:
        a.append([val])
    return a

# функция меняет вектор на кортеж
def vector_to_tuple(x):
    b=()
    for i in range(len(x)):
        b+=(x[i][0],)
    return b

# функция  возвращает сумму матриц
def getMatrixSum(a,b):
    if (len(a)!=len(b)) or (len(a[0])!=len(b[0])):
        return 'Матрицы нельзя сложить'
    s=copy.deepcopy(a)
    for i in range(len(a)):
        for j in range(len(a[0])):
            s[i][j]+=b[i][j]
    return s


# функция для проверки условия прекращения алгоритма в методе Ньютона
def proverka(delta_x):
    max=abs(delta_x[0][0])
    for i in range(len(delta_x)):
        if abs(delta_x[i][0])>max:
            max=abs(delta_x[i][0])
    return max
def solve_newton(systems, eps=0.00001) -> List[List[float]]:
    k=0
    # задаем какое-то начальное приближение
    x0 = [[1], [5]]

    # считаем матрицу якоби подставив значение из x0 (matrixa)
    matrix = MatrixIkobi(systems, x0)
    # print(matrix)
    # для деления F на матрицу якоби нужно найти обратную матрицу
    obratnay_matrix = getMatrixInverse(matrix)

    # найдем вектор F подставив в исходную систему значения x0 и домножим полученный вектор на -1
    # тк мы решили полставлять в систему кортеж, то преобразуем вектор в кортеж, а после подстановки вернем все как было
    x0 = vector_to_tuple(x0)
    F = getMatrixMult_to_1(systems(x0))
    x0 = tuple_to_vector(x0)
    # print(F)

    # ищем delta_x0 = obratnay_matrixa * F
    delta_x0 = getMatrixMult(obratnay_matrix, F)

    # ищем x1 = x0 + delta_x0
    k += 1
    x1 = getMatrixSum(x0, delta_x0)
    # print(x1)

    #далее повторяем те же дейсвия в цикле
    while proverka(delta_x0) > eps:
        # print(f'delta {k}')
        # print(proverka(delta_x0))
        matrix = MatrixIkobi(systems,x1)
        obratnay_matrix = getMatrixInverse(matrix)

        x1=vector_to_tuple(x1)
        F = getMatrixMult_to_1(systems(x1))
        x1=tuple_to_vector(x1)

        delta_x0 = getMatrixMult(obratnay_matrix, F)

        k += 1
        # print(f'x{k}')
        x0=x1
        x1 = getMatrixSum(x0, delta_x0)
        # print(x1)
    return x1


