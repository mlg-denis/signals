import indicators.compute as indct

# map the indicator names with the corresponding function
INDICATORS = {
    "SMA20": lambda data: indct.compute_sma(data["Close"], 20),
    "SMA50": lambda data: indct.compute_sma(data["Close"], 50),
    "EMA12": lambda data: indct.compute_ema(data["Close"], 12),
    "EMA26": lambda data: indct.compute_ema(data["Close"], 26),
    "MACD" : lambda data: indct.compute_macd(data["Close"]),
}

# indicators where crossovers are meaningful
CROSSOVER_PAIRS = [
    ("SMA20", "SMA50"),
    ("EMA12", "EMA26"),
    ("MACD", "Signal") # internal
]

VALID_INTERVALS = {
    "1d":  ["1m", "2m", "5m", "15m", "30m", "1h"],
    "5d":  ["1m", "2m", "5m", "15m", "30m", "1h"],
    "1mo": ["5m", "15m", "30m", "1h", "1d"],
    "3mo": ["1d", "1wk", "1mo"],
    "6mo": ["1d", "1wk", "1mo"],
    "1y":  ["1d", "1wk", "1mo"],
    "5y":  ["1wk", "1mo"],
    "10y": ["1mo"],
    "YTD": ["1d", "1wk", "1mo"],
    "Max": ["1mo"], 
}