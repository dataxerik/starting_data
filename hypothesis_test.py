import math
import random
from normal_distribution import normal_cdf
from normal_distribution import inverse_normal_cdf


def normal_approximation_to_binomial(n, p):
    # Find mu and sigma corresponding to a Binomial(n, p)
    mu = n * p
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


def normal_probability_below(lo, mu=0, sigma=1):
    return normal_cdf(lo, mu, sigma)


def normal_probability_above(lo, mu=0, sigma=1):
    return 1 - normal_cdf(lo, mu, sigma)


def normal_probability_between(lo, hi, mu=0, sigma=1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


def normal_probability_outside(lo, hi, mu=0, sigma=1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


def normal_upper_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z <= x) = probability"""
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability, mu=0, sigma=1):
    """returns the z for which P(Z >= x) = probability"""
    return inverse_normal_cdf(1 - probability, mu, sigma)


def normal_two_sided_bounds(probability, mu=0, sigma=1):
    """returns the symmetric, about the mean, bounds
    that contain the specified probability"""
    tail_probability = (1 - probability) / 2

    # upper bound should have a tail_probability above it
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)

    # lower bound should have a tail_probability below it
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)

    return lower_bound, upper_bound


def two_sided_p_value(x, mu=0, sigma=1):
    if x >= mu:
        # If x is greater than the mean, the tail is what's greater than x
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        # if x is less than the mean, the tail si what's less than x
        return 2 * normal_probability_below(x, mu, sigma)


def extreme_simulation():
    extreme_value_count = 0
    for _ in range(1000000):
        num_heads = sum(1 if random.random() < 0.5 else 0 for _ in range(1000))
        if num_heads >= 530 or num_heads <= 470:
            extreme_value_count += 1

    print(extreme_value_count / 1000000)


def run_expirement():
    """flip a fair coin 1000 times, True = heads, False = tails"""
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment):
    """using the 5% significance levels"""
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531


def run_p_test():
    random.seed(0)
    experiments = [run_expirement() for _ in range(1000)]
    num_rejections = len([experiment
                          for experiment in experiments
                          if reject_fairness(experiment)])

    print(num_rejections)


def main():
    mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)
    print(normal_two_sided_bounds(0.95, mu_0, sigma_0))

    # 95% bounds based on assumption p is 0.5
    lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

    # actual mu and sigma based on p = 0.55
    mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)

    # a type 2 error means we fail to reject the null hypothesis
    # which will happen when X si still in our original interval
    type_2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    print(power)

    hi = normal_upper_bound(0.95, mu_0, sigma_0)

    type_2_probability = normal_probability_below(hi, mu_1, sigma_1)
    power = 1 - type_2_probability
    print(power)

    print(two_sided_p_value(529.5, mu_0, sigma_0))

    # extreme_simulation()

    print(two_sided_p_value(531.5, mu_0, sigma_0))

    run_p_test()


if __name__ == "__main__": main()
