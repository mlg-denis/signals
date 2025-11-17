import pandas as pd
from definitions import CROSSOVER_PAIRS
from indicators.compute import detect_crossovers

DECIMAL_PLACES_OF_RETURN = 2

# long only backtest
def run_backtest(data: pd.DataFrame, 
                 enabled_indicators: dict[str, dict[str, pd.Series | pd.DataFrame | str]]):

    if data.empty:
        print("No data provided, skipping backtest")
        return pd.DataFrame(), 0.0, 0.0

    buy_and_hold_return = 100 * (data["Close"].iloc[-1] / data["Close"].iloc[0] - 1)
    buy_and_hold_return = round(buy_and_hold_return, DECIMAL_PLACES_OF_RETURN)

    if not enabled_indicators:
        print("No indicators enabled, skipping backtest.")
        return pd.DataFrame(), 0.0, buy_and_hold_return

    buydates, selldates = [], []
    for short, long in CROSSOVER_PAIRS:
        if short in enabled_indicators and long in enabled_indicators:
            s_series = enabled_indicators[short]["fn"](data)
            l_series = enabled_indicators[long]["fn"](data)
            crossovers: pd.Series = detect_crossovers(s_series, l_series)

            buydates.extend(crossovers.index[crossovers == 1])
            selldates.extend(crossovers.index[crossovers == -1])
            n = min(len(selldates), len(buydates))

    buydates = pd.Series(buydates)
    selldates = pd.Series(selldates)

    if buydates.empty or selldates.empty:
        print("No buy/sell signals to backtest.")
        return pd.DataFrame(), 0.0, buy_and_hold_return

    selldates = selldates[selldates > buydates.iloc[0]] # first sell happens after a buy
    buydates = buydates[buydates < selldates.iloc[-1]] # last buy happens before a sell
    buydates, selldates = buydates.iloc[:n], selldates.iloc[:n] # truncate to ensure pairings - redundant when using crossovers because they will be off by at most 1

    # drop the old date index to align by order instead of date label
    buyprices = data.loc[buydates, "Close"].reset_index(drop=True)
    sellprices = data.loc[selldates, "Close"].reset_index(drop=True)

    trades = pd.DataFrame({
        "Buy Date": buydates,
        "Buy Price": buyprices,
        "Sell Date": selldates,
        "Sell Price": sellprices,
        "Return": sellprices / buyprices - 1 # rate of return
    })
    print(trades)

    strategy_return = 100 * ((1 + trades["Return"]).prod() - 1)
    strategy_return = round(strategy_return, DECIMAL_PLACES_OF_RETURN)
    print(f"Return using strategy: {strategy_return}%")
    print(f"Return using buy and hold: {buy_and_hold_return}%")

    return(trades, strategy_return, buy_and_hold_return)