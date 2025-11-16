import matplotlib.pyplot as plt
import pandas as pd
from indicators.compute import detect_crossovers
from definitions import CROSSOVER_PAIRS

signal_size = 100

def init():
    plt.figure(figsize= (10,5))
    plt.xlabel("Date")
    plt.ylabel("Price")

def plot_series(series: pd.Series, label: str, style: str = "-", alpha: float = 1):
    plt.plot(series, style, label = label, alpha = alpha)

# calculates any crossovers that need to be calculated based on the given indicators
# plots any necessary crossover markers on the price line
def plot_crossovers(data, indicators, ax):
      
    for short, long in CROSSOVER_PAIRS:
        if short in indicators and long in indicators:
            crossovers = detect_crossovers(indicators[short],indicators[long])

            size = 7.5
            
            ax.plot(
                indicators[short].index[crossovers == 1],
                data["Close"][crossovers == 1],
                marker="^", color="green", linestyle="none", markersize = size, label="Bullish Crossover"
            )
            ax.plot(
                indicators[short].index[crossovers == -1],
                data["Close"][crossovers == -1],
                marker="v", color="red", linestyle="none", markersize = size, label="Bearish Crossover"
            )


def get_fig(data: pd.DataFrame, ticker: str,
            indicators: dict[str, pd.Series]):
    
    fig, ax = plt.subplots(figsize = (10,5))

    ax.plot(data["Close"], label="Price")

    for label, indicator in indicators.items():
        assert label, "You must supply a label with an indicator."
        ax.plot(indicator, label=label, linestyle = "--", alpha = 0.35)     

    plot_crossovers(data, indicators,ax)

    ax.set_title(ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price, USD")
    ax.legend()
    return fig