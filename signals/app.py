import streamlit as st
import financeinfo as fi
from backtesting import run_backtest
from plotter import get_fig
import indicators as indct

def main():
    index = "sp500"
    tickers = fi.get_index_constituents(index)
    ticker = st.selectbox("Select a ticker",
                        tickers,
                        index=None)

    if ticker:
        data = fi.fetch(ticker, period = "1y")
        ema12 = indct.compute_ema(data["Close"],12)
        ema26 = indct.compute_ema(data["Close"],26)
        fig = get_fig(data,ticker, ema12, "EMA12", ema26, "EMA26", True)
        st.pyplot(fig)

if __name__ == "__main__":
    main()    
