import pandas as pd

def compute_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window).mean()

def compute_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span = span, adjust = False).mean()

# crossover logic - check for each day whether short_avg > long_avg
# then to detect a crossover, check if this is different to the previous day 
def detect_crossovers(short_avg: pd.Series, long_avg: pd.Series) -> pd.Series:
    signal = (short_avg > long_avg).astype(int) # 1 if true; 0 if false
    return signal.diff() # return the crossovers