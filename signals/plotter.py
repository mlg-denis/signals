import matplotlib.pyplot as plt
import pandas as pd
from indicators.compute import detect_crossovers
from definitions import CROSSOVER_PAIRS, IndicatorType

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
            indicators: dict[str, dict[str, pd.Series | pd.DataFrame | str]]):
    
    overlays = {}
    oscillators: dict[str, dict[str, pd.Series | pd.DataFrame | str]] = {}
    for label, indicator in indicators.items():
        assert label, "You must supply a label with an indicator."
        match indicator["type"]:
            case IndicatorType.OVERLAY:
                overlays[label] = indicator
                #ax.plot(indicator, label=label, linestyle = "--", alpha = 0.35)
            case IndicatorType.OSCILLATOR:
                oscillators[label] = indicator

    nplots = 1 + len(oscillators) # 1 main plot and one per oscillator
    fig, axes = plt.subplots(nplots, sharex=True, figsize=(10, 5 + 2 * len(oscillators))) # height depends on number of oscillators

    if nplots == 1: # i.e. no oscillators
        axes = [axes]

    main_ax = axes[0]
    main_ax.plot(data["Close"], label= "Price", color="blue") # axes[0] is the main ax
    for label, indicator in overlays.items():
        main_ax.plot(indicator["fn"](data), label=label, linestyle="--", alpha=0.35)

    main_ax.legend()

    # oscillator: dict[str, series | df | str]
    oscillator_axes = axes[1:]
    for ax, oscillator in zip(oscillator_axes, oscillators.values()):
        df = oscillator["fn"](data)
        for col in df.columns:
            ax.plot(df[col], label=f"{col}")
            ax.legend()
        

    plot_crossovers(data, indicators, main_ax)

    main_ax.set_title(ticker)
    main_ax.set_xlabel("Date")
    main_ax.set_ylabel("Price, USD")
    main_ax.legend()
    return fig