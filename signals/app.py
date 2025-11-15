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
    ema12 = indct.compute_ema(data["Close"],12)
    ema26 = indct.compute_ema(data["Close"],26)
    fig = get_fig(data, ticker, ema12, "EMA12", ema26, "EMA26", True)
    st.pyplot(fig)

def main():
    st.set_page_config(layout="wide")

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

    st.markdown("""
    <style>
    .block-container {max-width: 1100px; padding-left: 2rem; padding-right: 2rem;}
    </style>
    """, unsafe_allow_html=True)    

    if ticker:
        handle(ticker, period, interval)        

if __name__ == "__main__":
    main()    
