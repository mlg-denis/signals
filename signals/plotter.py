import matplotlib.pyplot as plt
import pandas as pd
from indicators.compute import detect_crossovers
from definitions import CROSSOVER_PAIRS, IndicatorType

# turn any pd.DataFrames into multiple pd.Series
def flatten_results(results):
    flattened = {}
    for label, result in results.items():
        if isinstance(result, pd.DataFrame):
            for col in result.columns:
                flattened[col] = result[col]
        else: flattened[label] = result
    return flattened    

# calculates any crossovers that need to be calculated based on the given indicators
# plots any necessary crossover markers
def plot_crossovers(data, results, axes, oscillators):

    flattened = flatten_results(results)

    for ax_name, fast, slow in CROSSOVER_PAIRS:
        if fast not in flattened or slow not in flattened:
            continue
        
        crossovers = detect_crossovers(flattened[fast],flattened[slow])
        
        ax = None
        if ax_name == "MAIN":
            ax = axes[0]  # main price ax
            y = data["Close"]
        elif ax_name in oscillators:
                # find oscillator ax that matches one of the names
            ax_id = list(oscillators.keys()).index(ax_name)
            ax = axes[ax_id + 1] # skip main ax
            y = flattened[fast]

        if ax is None:
            raise ValueError(f"No matching ax found for crossover pair ({fast}, {slow})")    
            
        size = 7.5
        ax.plot(
            flattened[fast].index[crossovers == 1],
            y[crossovers == 1],
            marker="^", color="green", linestyle="none",
            markersize = size, label="Bullish Crossover"
        )
        ax.plot(
            flattened[fast].index[crossovers == -1],
            y[crossovers == -1],
            marker="v", color="red", linestyle="none",
            markersize = size, label="Bearish Crossover"
        )
        ax.legend()


def get_fig(data: pd.DataFrame, ticker: str,
            indicators: dict[str, dict[str, pd.Series | pd.DataFrame | str]]):
    
    results = {label: indicator["fn"](data) for label, indicator in indicators.items()}

    overlays = {k: v for k, v in indicators.items() if v["type"] == IndicatorType.OVERLAY}
    oscillators = {k: v for k, v in indicators.items() if v["type"] == IndicatorType.OSCILLATOR}

    nplots = 1 + len(oscillators) # 1 main plot and one per oscillator
    fig, axes = plt.subplots(nplots, sharex=False, figsize=(10, 5 + 2 * len(oscillators))) # height depends on number of oscillators

    if nplots == 1: # i.e. no oscillators
        axes = [axes]

    main_ax = axes[0]
    main_ax.plot(data["Close"], label= "Price", color="blue") # axes[0] is the main ax
    for label in overlays:
        result = results[label]
        if isinstance(result, pd.DataFrame):
            for col in result.columns:
                main_ax.plot(result[col], label=col, linestyle="--", alpha = 0.35)
        elif isinstance(result, pd.Series):        
            main_ax.plot(result, label=label, linestyle="--", alpha=0.35)
    main_ax.legend()

    oscillator_axes = axes[1:]
    for ax, label in zip(oscillator_axes, oscillators):
        result = results[label]
        # result could be either a Series or DataFrame depending on which oscillator is enabled
        if isinstance(result, pd.DataFrame):
            for col in result.columns:
                ax.plot(result[col], label=f"{col}")
        elif isinstance(result, pd.Series):
            ax.plot(result, label=label)
        ax.legend()    

    plot_crossovers(data, results, axes, oscillators)

    # deduplicate any repeated 'Bullish/Bearish Crossovers' on main ax legend
    handles, labels = main_ax.get_legend_handles_labels()
    unique = dict(zip(labels,handles))
    main_ax.legend(unique.values(), unique.keys())

    main_ax.set_title(ticker)
    main_ax.set_ylabel("Price, USD")

    return fig