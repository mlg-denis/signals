import streamlit as st
import financeinfo as fi
from backtesting import run_backtest
from plotter import get_fig
import indicators.compute as indct
from definitions import INDICATORS, VALID_INTERVALS

def validate_inputs(ticker: str, period: str, interval: str) -> str | None:
    if interval == "1m":
        assert period in ("1d", "5d"), "Cannot display 1m interval on periods larger than 5d."
    elif interval.endswith("m") or interval == "1h":
        assert period in ("1d", "5d", "1mo"), f"Cannot display {interval} interval on periods larger than 1mo."
    if not ticker or ticker.isspace():
        st.warning("Enter a ticker symbol to display chart data")
        return None
    return ticker.strip().upper() # so that "  nvda" shows as "NVDA"

def get_data(ticker, period, interval):
    try:
        data = fi.fetch(ticker, period.lower(), interval)
        if data.empty:
            st.warning(f"No price data found, symbol {ticker} may be delisted")
            return None
        return data
    except RuntimeError:
        st.error(f"Failed to fetch data for {ticker} - is Yahoo Finance down?")
    except Exception as e:
        st.error(f"Unexpected error while fetching {ticker} data: {e}")
    return None

def backtest(data, enabled_indicators):
    trades, strategy_return, buy_and_hold_return = run_backtest(data, enabled_indicators)
    st.write(f"Return using strategy: {strategy_return}%")
    st.write(f"Return with buy and hold: {buy_and_hold_return}%")
    if trades.empty:
        st.warning("No trades were generated for the current selection.")
    else:    
        st.dataframe(trades)

def handle(ticker, period, interval, indicator_states):
    ticker = validate_inputs(ticker, period, interval)
    if not ticker:
        return

    data = get_data(ticker, period, interval)
    if data is None:
        return

    # only plot those indicators that have their checkboxes enabled
    enabled_indicators = {label: INDICATORS[label] for label, enabled in indicator_states.items() if enabled}
    
    fig = get_fig(data, ticker, enabled_indicators)
    st.pyplot(fig)

    if st.button("Run backtest with selection"):
        backtest(data, enabled_indicators)

def load_css(filename: str):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# pulls the names from INDICATORS and creates a checkbox for each one
def indicator_checkboxes() -> dict[str, bool]:
    st.sidebar.header("Technical indicators")
    return {name: st.sidebar.checkbox(name) for name in INDICATORS.keys()}

def main():
    st.set_page_config(layout="wide")
    st.title("Dashboard")

    with st.container():
        ticker = st.text_input("Enter ticker symbol", value = None, placeholder="e.g. NVDA, SPY, 6869.HK")
        period = st.radio("Time range", list(VALID_INTERVALS.keys()), index=0, horizontal=True)
        interval = st.radio("Interval", VALID_INTERVALS[period], index=0, horizontal=True)

    st.divider()

    indicator_states = indicator_checkboxes()

    load_css("style.css")   

    handle(ticker, period, interval, indicator_states)        

if __name__ == "__main__":
    main()    
