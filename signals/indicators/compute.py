import pandas as pd

def compute_sma(closes: pd.Series, window: int) -> pd.Series:
    return closes.rolling(window).mean()

def compute_ema(closes: pd.Series, span: int) -> pd.Series:
    return closes.ewm(span = span, adjust = False).mean()

def compute_macd(closes: pd.Series) -> pd.DataFrame:
    macd = compute_ema(closes, 12) - compute_ema(closes, 26)
    signal = compute_ema(macd, 9)
    hist = macd - signal
    return pd.DataFrame({"MACD": macd, "Signal": signal, "MACD_hist": hist})

# crossover logic - check for each day whether short > long
# then to detect a crossover, check if this is different to the previous day 
def detect_crossovers(short: pd.Series, long: pd.Series) -> pd.Series:
    signal = (short > long).astype(int) # 1 if true; 0 if false
    return signal.diff() # return the crossovers