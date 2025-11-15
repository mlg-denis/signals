import streamlit as st
import financeinfo as fi
from backtesting import run_backtest
from plotter import get_fig
import indicators as indct

def handle(ticker, period, interval):
    if interval == "1m":
        assert period == "1d" or period == "5d", "Cannot display 1m interval on periods larger than 5d."
    elif interval[-1] == 'm' or interval == "1h":
        assert period == "1d" or period == "5d" or period == "1mo", f"Cannot display {interval} interval on periods larger than 1mo."
    
    data = fi.fetch(ticker, period, interval)

    indicators = {}
    for name, enabled in indicator_checkboxes().items():
        if not enabled:
            continue
        if "SMA" in name:
            window = int(name[3:])
            indicators[name] = indct.compute_sma(data["Close"], window)
        elif "EMA" in name:
            span = int(name[3:])
            indicators[name] = indct.compute_ema(data["Close"], span)

    fig = get_fig(data, ticker, indicators, True)
    st.pyplot(fig)

def load_css(filename: str):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def indicator_checkboxes():
    st.sidebar.header("Technical indicators")

    indicators = {
        "SMA20": st.sidebar.checkbox("SMA20"),
        "SMA50": st.sidebar.checkbox("SMA50"),
        "EMA12": st.sidebar.checkbox("EMA12"),
        "EMA26": st.sidebar.checkbox("EMA26"),
    }
    return indicators

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
        
        periods = ["1d","5d","1mo","3mo","6mo","YTD","1y","2y","5y","10y","Max"]
        period = st.radio(
            "Time range",
            periods,
            index=6,
            horizontal=True
        ).lower()

        intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo"]
        interval = st.radio(
            "Interval",
            intervals,
            index=7,
            horizontal=True
        )

    st.divider()

    load_css("style.css")   

    if ticker:
        handle(ticker, period, interval)        

if __name__ == "__main__":
    main()    
