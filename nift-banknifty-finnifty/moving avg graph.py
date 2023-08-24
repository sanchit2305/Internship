
import pandas as pd
import matplotlib.pyplot as plt
nifty_data = pd.read_csv('^NSEI.csv')
nifty_data['Date'] = pd.to_datetime(nifty_data['Date'])
nifty_data.sort_values(by='Date', ascending=True, inplace=True)

nifty_data['5-day MA'] = nifty_data['Close'].rolling(window=5).mean()


nifty_data['7-day MA'] = nifty_data['Close'].rolling(window=7).mean()

plt.figure(figsize=(12, 6))
plt.plot(nifty_data['Date'], nifty_data['Close'], label='Nifty Close', color='blue')
plt.plot(nifty_data['Date'], nifty_data['5-day MA'], label='5-day MA', color='orange')
plt.plot(nifty_data['Date'], nifty_data['7-day MA'], label='7-day MA', color='red')


plt.xlabel('Date')
plt.ylabel('Price')
plt.title('Nifty Moving Averages')
plt.legend()

plt.show() 