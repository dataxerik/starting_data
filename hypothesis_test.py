from normal_distribution import normal_cdf

def normal_approximation_to_binomial(n, p):
    #Find mu and sigma corresponding to a Binomial(n, p)
    mu = n * p
    sigma = math.sqrt(p * (1-p) * n)
    return mu, sigma

