import math
from functools import reduce


def vector_add(v, w):
    """adds corresponding elements"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def vector_subtract(v, w):
    """subtracts corresponding elements"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]


"""
def vector_sum(vectors):
    Sums all corresponding elements
    result = vectors[0]
    for vector in vectors:
        result = vector_add(result, vector)
    return result
"""


def vector_sum(vectors):
    return reduce(vector_add, vectors)


# vector_sum = partial(reduce, vector_add)

def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]


def vector_mean(vectors):
    """Compute the vector whose ith element is the mean of the
    ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1 / n, vector_sum(vectors))


def dot(v, w):
    """v_1 * w_1 + .... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    """v_1 * v_1 + ... + v_n * w_n"""
    return dot(v, v)


def magnitude(v):
    return math.sqrt(sum_of_squares(v))


def squared_distance(v, w):
    """(v_1 - w_1) ** 2 + .... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))


def distance(v, w):
    return magnitude(vector_subtract(v, w))


def shape(A):
    num_rows = len(A)
    num_cols = len(A[0] if A else 0)
    return num_rows, num_cols


def get_row(A, i):
    return A[i]


def get_column(A, j):
    return [A_i[j] for A_i in A]


def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i, j)th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_rows)]


def is_diagonal(i, j):
    """1's on the diagonal, 0's else where"""
    return 1 if i == j else 0