import matplotlib.pyplot as plt
import pandas as pd
from indicators import detect_crossovers

signal_size = 100

def init():
    plt.figure(figsize= (10,5))
    plt.xlabel("Date")
    plt.ylabel("Price")

def plot_series(series: pd.Series, label: str, style: str = "-", alpha: float = 1):
    plt.plot(series, style, label = label, alpha = alpha)

def plot_crossovers(data: pd.DataFrame, column: str):
    # takes all the dates (and the prices @ close on those dates) where a crossover
    # has occurred and plots a scatter plot with a marker for the bullish signal
    plt.scatter(
        data.index[data[column] == 1],
        data["Close"][data[column] == 1],
        marker = "^", color = "green", s = signal_size, label = "Bullish Crossover"
    )

    # same as above but for bearish signals
    plt.scatter(
        data.index[data[column] == -1],
        data["Close"][data[column] == -1],
        marker = "v", color = "red", s = signal_size, label = "Bearish Crossover"
    )

def get_fig(data: pd.DataFrame, ticker: str,
            indicators: dict[str, pd.Series],
            plot_crossovers: bool = False):
    
    fig, ax = plt.subplots(figsize = (10,5))

    ax.plot(data["Close"], label="Price")

    for label, indicator in indicators.items():
        assert label, "You must supply a label with an indicator."
        ax.plot(indicator, label=label, linestyle = "--", alpha = 0.35)     

    ax.set_title(ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price, USD")
    ax.legend()
    return fig