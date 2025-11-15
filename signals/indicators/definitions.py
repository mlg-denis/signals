import indicators.compute as indct

# map the indicator names with the corresponding function
INDICATORS = {
    "SMA20":  lambda data: indct.compute_sma(data["Close"], 20),
    "SMA50":  lambda data: indct.compute_sma(data["Close"], 50),
    "EMA12":  lambda data: indct.compute_ema(data["Close"], 12),
    "EMA26":  lambda data: indct.compute_ema(data["Close"], 26),
}