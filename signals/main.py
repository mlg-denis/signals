import financeinfo as fi
import indicators as indc
import plotter as p
import backtesting as bt

def main():
    '''
    ticker = "6896.HK"
    data = fi.fetch(ticker)
    closes = data["Close"]

    sma20 = indc.compute_sma(closes, 20)
    sma50 = indc.compute_sma(closes, 50)
    ema12 = indc.compute_ema(closes, 12)
    ema26 = indc.compute_ema(closes, 26)
   
    column = "Crossover"
    data[column] = indc.detect_crossovers(sma20, sma50)

    bt.run_backtest(data, column)
    '''
    print(fi.get_index_constituents("sp500"))

if __name__ == "__main__":
    main()