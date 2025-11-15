import financeinfo
import indicators as indc
import plot as p
import backtesting

def main():
    ticker = "TSLA"
    info = financeinfo.fetch(ticker)
    closes = info["Close"]

    sma20 = indc.compute_sma(closes, 20)
    sma50 = indc.compute_sma(closes, 50)
    ema12 = indc.compute_ema(closes, 12)
    ema26 = indc.compute_ema(closes, 26)
   
    column = "Crossover"
    info[column] = indc.detect_crossovers(sma20, sma50)

    backtesting.run_backtest(info, column)

    p.init()
    p.plot_series(closes, "Price", "-", 0.7)
    p.plot_series(ema12, "EMA12", "--", 0.35)
    p.plot_series(ema26, "EMA26", "--", 0.35)
    p.plot_crossovers(info, column)
    p.title(ticker)
    p.show()

if __name__ == "__main__":
    main()