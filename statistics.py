from __future__ import division
import math
import random
import matplotlib.pyplot as plt
from collections import Counter
from linear_algebra import sum_of_squares, dot, shape, get_column, get_row, make_matrix


def mean(x):
    return sum(x) / len(x)


def median(x):
    """finds the 'middle-most' value of v"""
    n = len(x)
    sorted_x = sorted(x)
    midpoint = n // 2

    if n % 2 == 1:
        return sorted_x[midpoint]
    else:
        lo = midpoint - 1
        hi = midpoint
        return (sorted_x[lo] + sorted_x[hi]) / 2


def quantile(x, p):
    """returns the pth-percentile value in x"""
    p_index = int(p * len(x))
    return sorted(p)[p_index]


def mode(x):
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.interitems() if count == max_count]


def data_range(x):
    return max(x) - min(x)


def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)


def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    """assume x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)


def standard_deviation(x):
    return math.sqrt(variance(x))


def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)


def correlation(x, y):
    stddev_x = standard_deviation(x)
    stddev_y = standard_deviation(y)
    if stddev_y > 0 and stddev_x > 0:
        return covariance(x, y) / stddev_x / stddev_y
    else:
        return 0  # if no variation, correlation is zero

