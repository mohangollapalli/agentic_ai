import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the stock tickers
tickers = ['META', 'AAPL']

# Get the date range (last 12 months)
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Fetch data for META and APPLE
data = yf.download(tickers, start=start_date, end=end_date)

# DEBUG: Print the columns to identify available ones
print("Available columns in the data:", data.columns)

# Check if 'Adj Close' is available; if not, fall back to 'Close'
if 'Adj Close' in data.columns:
    data = data['Adj Close']
else:
    data = data['Close']

# Plot the stock prices
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(data[ticker], label=ticker, linewidth=2)  # Plot data for each ticker
plt.title("Stock Prices of META and Apple (Last 12 Months)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()