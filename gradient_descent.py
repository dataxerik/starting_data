import random
import matplotlib.pyplot as plt
from functools import partial
from linear_algebra import distance

def sum_of_squares(v):
    """computes teh sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)


def difference_quotient(f, x, h):
    return (f(x + h) - f(x)) / h


def square(x):
    return x * x


def derivative(x):
    return 2 * x


def partial_difference_quotient(f, v, i, h):
    """Compute the ith partial difference quotient of f at v"""
    w = [v_j + (h if j == i else 0) for j, v_j in enumerate(v)] # add h to just the ith element of v
    return (f(w) - f(v)) / h


def estimate_gradient(f, v, h=0.00001):
    return [partial_difference_quotient(f, v, i, h) for i, _ in enumerate(v)]


def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [v_i + step_size * direction_i for v_i, direction_i in zip(v, direction)]


def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]


def run_experiment():
    v = [random.randint(-10, 10) for i in range(3)]
    tolerance = 0.0000001

    while True:
        gradient = sum_of_squares_gradient(v)
        next_v = step(v, gradient, -0.01)
        if distance(next_v, v) < tolerance:
            break
        v = next_v
    print(v)

def main():
    """
    derivative_estimate = partial(difference_quotient, square, h = 0.00001)
    x = range(-10, 10)
    plt.title("Actual Derivatives vs. Estimates")
    plt.plot(x, list(map(derivative, x)), 'rx', label='Actual') # red x = rx
    plt.plot(x, list(map(derivative_estimate, x)), 'b+', label='Estimate')

    plt.legend(loc=9)
    plt.show()"""
    run_experiment()


if __name__ == "__main__": main()