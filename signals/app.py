import streamlit as st
from financeinfo import fetch
from backtesting import run_backtest
from plotter import get_fig
import indicators as indct

def main():
    tickers = ["AAPL", "NVDA", "TSLA"]
    ticker = st.selectbox("Select a ticker",
                        tickers,
                        index=None)

    if ticker:
        data = fetch(ticker, period = "1y")
        ema12 = indct.compute_ema(data["Close"],12)
        ema26 = indct.compute_ema(data["Close"],26)
        fig = get_fig(data,ticker, ema12, "EMA12", ema26, "EMA26", True)
        st.pyplot(fig)

if __name__ == "__main__":
    main()    
