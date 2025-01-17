import math
from scipy.stats import norm
import yfinance as yf
import numpy as np
from datetime import datetime
import pandas as pd

def black_scholes(S, K, T, r, vol, option_type="call"):
    d1 = (math.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))
    d2 = d1 - vol * math.sqrt(T)
    #print(f"D1 Value: {round(d1,4)}")
    #print(f"D2 Value: {round(d2,4)}")
    if option_type == "call":
        # Calculate call option price (Probability that S at D1 > K at D2)
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        # Calculate put option price (Probability that S at D1 < K at D2)
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

S = 42 # Underlying Price
K = 40 # Strike Price
T = 0.5 # Time to Expiration/Maturity
r = 0.1 # Risk-Free Rate
vol = 0.2 # Volatility (sigma)
# print(f"Call Option Price: {round(black_scholes(S, K, T, r, vol, option_type="call"),2)}")
# print(f"Put Option Price: {round(black_scholes(S, K, T, r, vol, option_type="put"),2)}")

ticker = input("Input Ticker (Default: AAPL): \n")
if not ticker:
    ticker = "AAPL"
ticker = yf.Ticker(ticker)

data = ticker.history(period="1d")  # Gets tickers latest data
S = data['Close'].iloc[-1]  # Gets latest close price


options = ticker.options  # Get all option expiration dates
# print(options) # Prints available expiration dates
if not options:
    raise ValueError("No options data available for this ticker.")
exp_date = datetime.strptime(options[1], "%Y-%m-%d") # Get the second earliest expiration date as a date (change this to allow user to select)


opt_chain = ticker.option_chain(options[1]) #Get the second earliest expiration date as an option chain
calls = opt_chain.calls #Gets all calls from option chain
puts = opt_chain.puts #Gets all puts from option chain

# Find the closest call strike price
closest_call = calls.iloc[(calls['strike'] - S).abs().idxmin()]
K = closest_call['strike']

# Find the put strike price
closest_put = puts.iloc[(puts['strike'] - S).abs().idxmin()]


# Calculate time to expiration
cur_date = datetime.now()
T = (exp_date - cur_date).days / 365.0


r = 0.03  # Assuming 3% annualized risk-free rate


# Calculate historical volatility (Time period is 1 year)
period = "1y"
stock_data = ticker.history(period=period)
stock_data['Daily Return'] = stock_data["Close"].pct_change()
vol = stock_data['Daily Return'].std() * np.sqrt(252)

# Calculate predicted option prices
call_price = black_scholes(S, K, T, r, vol, option_type="call")
put_price = black_scholes(S, K, T, r, vol, option_type="put")

# Prepare data for table output
summary_data = {
    "Metric": [
        "Underlying Price",
        "Strike Price (Closest Call)",
        "Strike Price (Closest Put)",
        "Time to Expiration (Years)",
        "Risk-Free Rate",
        "Historical Volatility",
        "Predicted Call Price",
        "Predicted Put Price",
    ],
    "Value": [
        f"${S:.2f}",
        f"${closest_call['strike']:.2f}",
        f"${closest_put['strike']:.2f}",
        f"{T:.4f}",
        f"{r:.2%}",
        f"{vol:.2%}",
        f"${call_price:.2f}",
        f"${put_price:.2f}",
    ],
}

call_option_data = {
    "Strike Price": closest_call['strike'],
    "Last Price": closest_call['lastPrice'],
    "Actual-Expected": round(closest_call['lastPrice']-call_price,3),
    "Volume": closest_call['volume'],
}

put_option_data = {
    "Strike Price": closest_put['strike'],
    "Last Price": closest_put['lastPrice'],
    "Actual-Expected": round(closest_put['lastPrice']-put_price,3),
    "Volume": closest_put['volume'],
}

# Create DataFrames
summary_table = pd.DataFrame(summary_data)
call_table = pd.DataFrame([call_option_data], index=["Closest Call Option"])
put_table = pd.DataFrame([put_option_data], index=["Closest Put Option"])

# Display the data

print(f"\nSummary Table for {ticker.info['longName']} :")
print(summary_table)

print("\nCall Option Analysis:")
print(call_table)

print("\nPut Option Analysis:")
print(put_table)
