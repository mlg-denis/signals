import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

ticker = "AAPL"
data = yf.download(ticker, period = "1y", interval = "1d")

# calculating SMAs from data
data["SMA20"] = data["Close"].rolling(20).mean()
data["SMA50"] = data["Close"].rolling(50).mean()

# calculating EMAs from data
data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()

# crossover logic - check for each day whether short_avg > long_avg
# then to detect a crossover, check if this is different to the previous day 
def detect_crossovers(short_avg, long_avg):
    
    signal = (short_avg > long_avg).astype(int) # 1 if true; 0 if false
    return signal.diff() # return the crossovers

data["Crossover"] = detect_crossovers(data["EMA12"], data["EMA26"])

plt.figure(figsize=(10, 5))

plt.plot(data["Close"], label="Price")
plt.plot(data["EMA12"], label="12-day EMA", linestyle="--")
plt.plot(data["EMA26"], label="26-day EMA", linestyle="--")

# takes all the dates (and the prices @ close on those dates) where a crossover
# has occurred and plots a scatter plot with a marker for the bullish signal
plt.scatter(
    data.index[data["Crossover"] == 1],
    data["Close"][data["Crossover"] == 1],
    marker = "^", color = "green", label = "Bullish Crossover"
)

# same as above but for bearish signals
plt.scatter(
    data.index[data["Crossover"] == -1],
    data["Close"][data["Crossover"] == -1],
    marker = "v", color = "red", label = "Bearish Crossover"
)

plt.legend()
plt.title(f"{ticker} Moving Average Crossover")
plt.show()

