import yfinance as yf
import pandas as pd

# get ticker data from yf, with default fallback params
# if ticker isn't found raise an exception
def fetch(ticker: str, period:str = "1y", interval:str = "1d", auto_adjust: bool = True) -> pd.DataFrame:
    try:
        data = yf.download(ticker, period = period, interval = interval, auto_adjust=auto_adjust)
        if (isinstance(data.columns, pd.MultiIndex)):
            data.columns = data.columns.get_level_values(0) # flatten the MultiIndex so we get the data we care for
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {ticker}: {e}")

# function to get the constituents of an index via the FMP API    
# index examples: nasdaq, sp500, ftse_100, dax    
def get_index_constituents(index: str) -> list[str]:
    url = f"https://www.slickcharts.com/{index}"
    try:
        dfs = pd.read_html(io=url)
    except Exception as e:
        print(f"Error gathering {index} constituents: {e}")    
    else:
        data = dfs[0] # this happens to be the table containing the constituents
        return list(data["Symbol"]) 