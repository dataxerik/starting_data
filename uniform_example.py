def uniform_pdf(x):
    return 1 if x >= 0 and x < 1 else 0

def uniform_cdf(x):
    if x < 0: return 0 # Unif is never less than zero
    elif x < 1: return x # P(X <= 0.4) = 0.4
    else: return 1 # Unif is always else than 1