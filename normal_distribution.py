from __future__ import division
import math
import matplotlib.pyplot as plt


def normal_pdf(x, mu=0, sigma=1):
    sqrt_two_pi = math.sqrt(2 * math.pi)
    return (math.exp(-(x - mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))


def normal_cdf(x, mu=0, sigma=1):
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2


def inverse_normal_cdf(p, mu=0, sigma=1, tolerance=0.00001):
    # if not a standard, compute standard and re-scale
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)

    low_z, low_p = -10.0, 0
    hi_z, hi_p = 10.0, 1
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2  # midpoint
        mid_p = normal_cdf(mid_z)  # and the cdf value there
        if mid_p < p:
            # midpoint is still to low, search above it
            low_z, low_p = mid_z, mid_p
        elif mid_p > p:
            hi_z, hi_p = mid_z, mid_p
        else:
            break
    return mid_z


def main():
    '''
    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_pdf(x, sigma=1) for x in xs],'-',label='mu=0,sigma=1')
    plt.plot(xs, [normal_pdf(x, sigma=2) for x in xs], '-', label='mu=0,sigma=2')
    plt.plot(xs, [normal_pdf(x, sigma=0.5) for x in xs], '-', label='mu=0,sigma=0.5')
    plt.plot(xs, [normal_pdf(x, mu=1) for x in xs], '-', label='mu=1,sigma=1')
    plt.legend()
    plt.title("Various Normal pdfs")
    plt.show()

    xs = [x / 10.0 for x in range(-50, 50)]
    plt.plot(xs, [normal_cdf(x, sigma=1) for x in xs],'-',label='mu=0,sigma=1')
    plt.plot(xs, [normal_cdf(x, sigma=2) for x in xs], '-', label='mu=0,sigma=2')
    plt.plot(xs, [normal_cdf(x, sigma=0.5) for x in xs], '-', label='mu=0,sigma=0.5')
    plt.plot(xs, [normal_cdf(x, mu=1) for x in xs], '-', label='mu=1,sigma=1')
    plt.title("Various Normal cdfs")
    plt.show()'''
    print(inverse_normal_cdf(900))


if __name__ == "__main__": main()
