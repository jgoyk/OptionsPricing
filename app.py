import math
from scipy.stats import norm

S = 42 # Underlying Price
K = 40 # Strike Price
T = 0.5 # Time to Expiration/Maturity
r = 0.1 # Risk-Free Rate
vol = 0.2 # Volatility (sigma)

d1 = (math.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))
d2 = d1 - vol * math.sqrt(T)

# Calculate call option price 
# (Probability that S at D1 > K at D2)
C = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# Calculate put option price
# (Probability that S at D1 < K at D2)

P = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

print(f"D1 Value: {round(d1,4)}")
print(f"D2 Value: {round(d2,4)}")
print(f"Call Option Price: {round(C,2)}")
print(f"Put Option Price: {round(P,2)}")
