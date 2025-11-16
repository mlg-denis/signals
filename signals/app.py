import streamlit as st
import financeinfo as fi
from backtesting import run_backtest
from plotter import get_fig
import indicators.compute as indct
from definitions import INDICATORS, VALID_INTERVALS

def handle(ticker, period, interval):
    if interval == "1m":
        assert period == "1d" or period == "5d", "Cannot display 1m interval on periods larger than 5d."
    elif interval[-1] == 'm' or interval == "1h":
        assert period == "1d" or period == "5d" or period == "1mo", f"Cannot display {interval} interval on periods larger than 1mo."
    
    data = fi.fetch(ticker, period.lower(), interval) # rectify difference between display case and parameter case ("Max" vs "max")

    # for the checked boxes, apply their respective functions to the data and keep the result to add to the graph
    indicators = {}
    for label, enabled in indicator_checkboxes().items():
        if not enabled:
            continue
        indicators[label] = INDICATORS[label](data)

    # flatten potential dictionaries, e.g. MACD
    flattened = {}
    for label, value in indicators.items():
        if isinstance(value, dict):
            flattened.update(value) # add the dictionary to flattened
        else:
            flattened[label] = value    

    fig = get_fig(data, ticker, flattened)
    st.pyplot(fig)

def load_css(filename: str):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# pulls the names from INDICATORS and creates a checkbox for eacah one
def indicator_checkboxes() -> dict[str, bool]:
    st.sidebar.header("Technical indicators")
    return {name: st.sidebar.checkbox(name) for name in INDICATORS.keys()}

def main():
    st.set_page_config(layout="wide")
    st.title("Dashboard")

    #add_checkboxes()

    with st.container():
        index = "sp500"
        tickers = fi.get_index_constituents(index) + ["VUAG.L"]
        ticker = st.selectbox(
            "Select a ticker",
            tickers,
            index=0
        )
        
        period = st.radio(
            "Time range",
            list(VALID_INTERVALS.keys()),
            index=0,
            horizontal=True
        )

        interval = st.radio(
            "Interval",
            VALID_INTERVALS[period],
            index=0,
            horizontal=True
        )

    st.divider()

    load_css("style.css")   

    if ticker:
        handle(ticker, period, interval)        

if __name__ == "__main__":
    main()    
