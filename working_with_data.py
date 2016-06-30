import math
import random
import matplotlib.pyplot as plt
from collections import Counter
from normal_distribution import inverse_normal_cdf

def bucketsize(point, bucket_size):
    """floor the point to the next lower multiple of bucket size"""
    return bucket_size * math.floor(point / bucket_size)

def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketsize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(histogram.keys(), histogram.values(), width=bucket_size)
    plt.title()
    plt.show()

def plot_uni_nor():
    random.seed(0)

    # U(-100, 100)
    uniform = [200 * random.random() - 100 for _ in range(10000)]

    # N(0, 57)
    normal = [57 * inverse_normal_cdf(random.random()) for _ in range(10000)]

    plot_histogram(uniform, 10, "Uniform Histogram")

    plot_histogram(normal, 10, "Normal Histogram")

def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

xs = [random_normal() for _ in range(1000)]
ys1 = [x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]

plt.scatter(xs, ys1, marker='.', color='black', label='ys1')
plt.scatter(xs, ys2, marker='.', color='gray', label='ys2')
plt.xlabel('xs')
plt.ylabel('ys')
plt.legend(loc=9)
plt.title("Very different joint distribution")
plt.show()

print("correlation of xs and ys1 {} and correlation of xs and ys2 {}".format(correlation(xs, ys1),
                                                                             correlation()))