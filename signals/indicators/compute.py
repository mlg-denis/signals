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

def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    rsi.name = "RSI"
    return rsi

def compute_stochastic(high: pd.Series, low: pd.Series, close: pd.Series,
                       k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    lowest_low = low.rolling(window=k_period, min_periods=k_period).min()
    highest_high = high.rolling(window=k_period, min_periods=k_period).max()

    percent_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    percent_d = percent_k.rolling(window=d_period, min_periods=d_period).mean()

    df = pd.DataFrame({
        "STOCH_%K": percent_k,
        "STOCH_%D": percent_d
    })
    return df

def compute_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window=period, min_periods=period).mean()
    return atr.rename("ATR")

def compute_bbands(close: pd.Series, period: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    sma = close.rolling(window=period, min_periods=period).mean()
    std = close.rolling(window=period, min_periods=period).std()

    upper = sma + num_std * std
    lower = sma - num_std * std

    bands = pd.DataFrame({
        "BB_Upper": upper,
        "BB_Middle": sma,
        "BB_Lower": lower
    })
    return bands

def compute_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    direction = close.diff().fillna(0)
    sign = direction.apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    obv = (sign * volume).cumsum()
    return obv.rename("OBV")

# crossover logic - check for each day whether fast > slow
# then to detect a crossover, check if this is different to the previous day 
def detect_crossovers(fast: pd.Series, slow: pd.Series) -> pd.Series:
    signal = (fast > slow).astype(int) # 1 if true; 0 if false
    return signal.diff() # return the crossovers