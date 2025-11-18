**Stock Screener Dashboard**

An interactive web dashboard app for visualising and backtesting technical indicators on historical stock price data.
Built with Python, Streamlit, Pandas, yfinance, and Matplotlib.

**What It Does**
- Fetches price data from Yahoo Finance (yfinance).
- Calculates common indicators (SMA, EMA, MACD, RSI, Bollinger Bands, etc.).
- Plots indicators dynamically, highlighting bullish and bearish crossover.
- Includes a backtesting engine for crossover-based strategies.


Dashboard:

![Dashboard](https://github.com/user-attachments/assets/c06d9805-ba78-4160-b656-2f93454b7a94)

Example chart with indicators:

![Chart with indicators](https://github.com/user-attachments/assets/43c3047f-e515-4722-ae61-cdc4daf1a64e)

Example backtest:

![Backtest example](https://github.com/user-attachments/assets/70d1db55-9800-4673-9f68-499561217a3c)

**Technical Highlights**
- Modular design:
  - compute.py - Vectorised indicator functions
  - backtesting.py - Crossover logic and trade simulation
  - plotter.py - Matplotlib-based figure composition
  - dashboard.py - Streamlit front-end
- Designed for readability and efficiency (indicators are only computed once).
- Built from scratch without external trading libraries.

By Marc Denis - Computer Science student at University of Oxford

mlg-denis@outlook.com
