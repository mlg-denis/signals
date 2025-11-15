import yfinance as yf
import pandas as pd

# get ticker data from yf, with default fallback params
# if ticker isn't found raise an exception
def fetch(ticker: str, period:str = "1y", interval:str = "1d", auto_adjust: bool = True) -> pd.DataFrame:
    try:
        data = yf.download(ticker, period = period, interval = interval, auto_adjust=auto_adjust)
        if (isinstance(data.columns, pd.MultiIndex)):
            data.columns = data.columns.get_level_values(0) # flatten the MultiIndex so we get the data we care for
        print(data.columns)
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {ticker}: {e}" )