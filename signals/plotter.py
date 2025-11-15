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
            short_avg: pd.Series = None, short_label: str = None,
            long_avg: pd.Series = None, long_label: str = None,
            plot_crossovers: bool = False):
    
    fig, ax = plt.subplots(figsize = (10,5))

    ax.plot(data["Close"], label = "Price")

    if not short_avg.empty:
        assert short_label, "You must supply a label when providing short_avg."
        ax.plot(short_avg, label = short_label, linestyle = "--")

    if not long_avg.empty:
        assert long_label, "You must supply a label when providing long_avg."
        ax.plot(long_avg, label = long_label, linestyle = "--")

    if plot_crossovers:
        
        assert not short_avg.empty, "You must supply a short average to plot crossover points."
        assert not long_avg.empty, "You must supply a long average to plot crossover points."
        
        try:
            data["Crossover"] = detect_crossovers(short_avg, long_avg)
            size = 7.5

            ax.plot(
                data.index[data["Crossover"] == 1],
                data["Close"][data["Crossover"] == 1],
                marker="^", color="green", linestyle="none", markersize = size, label="Bullish Crossover"
            )

            ax.plot(
                data.index[data["Crossover"] == -1],
                data["Close"][data["Crossover"] == -1],
                marker="v", color="red", linestyle="none", markersize = size, label="Bearish Crossover"
            )
        except Exception as e:
            print(f"Attempt to plot crossover failed: {e}")

    ax.set_title(ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price, USD")
    ax.legend()
    return fig  