import matplotlib.pyplot as plt
import pandas as pd
from indicators.compute import detect_crossovers
from definitions import CROSSOVER_PAIRS, IndicatorType

#indicators: dict[str, dict[str, pd.Series | pd.DataFrame | str]
def flatten_indicators(indicators, data: pd.DataFrame) -> dict[str, pd.Series]:
    flattened = {}
    for label, indicator in indicators.items():
        result = indicator["fn"](data)

        if isinstance(result, pd.DataFrame):
            for col in result.columns:
                flattened[col] = result[col]
        else: flattened[label] = result
    return flattened    

# calculates any crossovers that need to be calculated based on the given indicators
# plots any necessary crossover markers
def plot_crossovers(data, indicators, axes, overlays, oscillators):

    flattened = flatten_indicators(indicators,data) # turn pd.DataFrames into pd.Series
      
    for short, long in CROSSOVER_PAIRS:
        if short in flattened and long in flattened:
            crossovers = detect_crossovers(flattened[short],flattened[long])

            size = 7.5

            if short in overlays or long in overlays:
                ax = axes[0]  # main price axis
                y = data["Close"]
            else:
                # find oscillator axis that matches one of the names
                ax = next((a for a, (label, ind) in zip(axes[1:], oscillators.items())
                        if label in (short, long)), axes[0])
                y = flattened[short]
            
            ax.plot(
                flattened[short].index[crossovers == 1],
                y[crossovers == 1],
                marker="^", color="green", linestyle="none", markersize = size, label="Bullish Crossover"
            )
            ax.plot(
                flattened[short].index[crossovers == -1],
                y[crossovers == -1],
                marker="v", color="red", linestyle="none", markersize = size, label="Bearish Crossover"
            )
            ax.legend()


def get_fig(data: pd.DataFrame, ticker: str,
            indicators: dict[str, dict[str, pd.Series | pd.DataFrame | str]]):
    
    overlays = {}
    oscillators: dict[str, dict[str, pd.Series | pd.DataFrame | str]] = {}
    for label, indicator in indicators.items():
        assert label, "You must supply a label with an indicator."
        match indicator["type"]:
            case IndicatorType.OVERLAY:
                overlays[label] = indicator
            case IndicatorType.OSCILLATOR:
                oscillators[label] = indicator

    nplots = 1 + len(oscillators) # 1 main plot and one per oscillator
    fig, axes = plt.subplots(nplots, sharex=False, figsize=(10, 5 + 2 * len(oscillators))) # height depends on number of oscillators

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

    plot_crossovers(data, indicators, axes, overlays, oscillators)

    main_ax.set_title(ticker)
    main_ax.set_ylabel("Price, USD")
    main_ax.legend()
    return fig