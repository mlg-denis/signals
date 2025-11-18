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
    
    signals = pd.Series(0, index=data.index) 

    for parent, fast, slow in CROSSOVER_PAIRS:
        if fast in enabled_indicators and slow in enabled_indicators:
            f_series = enabled_indicators[fast]["fn"](data)
            s_series = enabled_indicators[slow]["fn"](data)
        elif parent in enabled_indicators:
            result = enabled_indicators[parent]["fn"](data)
            f_series, s_series = result[fast], result[slow]
        else:
            continue    

        aligned = pd.concat([f_series, s_series], axis=1, join="inner").dropna() # only consider points when both series have values
        f_series, s_series = aligned.iloc[:, 0], aligned.iloc[:, 1]    
        crossovers = detect_crossovers(f_series, s_series).shift(1).fillna(0) # can only trade on the interval after crossover detected

        signals = signals.add(crossovers.reindex(signals.index, fill_value=0), fill_value=0)
        # signals is now filled with -1 (exit position), 0 (status quo), 1 (enter position) 

    trades = []
    in_position = False
    entry_date = None
    entry_price = None

    for date, signal in signals.items():
        price = data.loc[date, "Close"]

        if not in_position and signal == 1:
            entry_date = date
            entry_price = price
            in_position = True

        elif in_position and signal == -1:
            exit_date = date
            exit_price = price
            trades.append({
                "Entry Date": entry_date,
                "Entry Price": entry_price,
                "Exit Date": exit_date,
                "Exit Price": exit_price,
                "Return": (exit_price / entry_price) - 1
            })
            entry_date = None
            entry_price = None
            in_position = False

    if in_position: # if last signal is a buy signal, force close position at end of time period
        exit_date = data.index[-1]
        exit_price = data["Close"].iloc[-1]
        trades.append({
            "Entry Date": entry_date,
            "Entry Price": entry_price,
            "Exit Date": exit_date,
            "Exit Price": exit_price,
            "Return": (exit_price / entry_price) - 1
        })

    trades = pd.DataFrame(trades)     

    strategy_return = 100 * ((1 + trades["Return"]).prod() - 1)
    strategy_return = round(strategy_return, DECIMAL_PLACES_OF_RETURN)
    print(f"Return using strategy: {strategy_return}%")
    print(f"Return using buy and hold: {buy_and_hold_return}%")

    return(trades, strategy_return, buy_and_hold_return)