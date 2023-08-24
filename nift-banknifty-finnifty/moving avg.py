import pandas as pd


nifty_data = pd.read_csv('^NSEI.csv')


nifty_data['Date'] = pd.to_datetime(nifty_data['Date'])


nifty_data.sort_values(by='Date', ascending=True, inplace=True)


nifty_data['5-day MA'] = nifty_data['Close'].rolling(window=5).mean()


nifty_data['7-day MA'] = nifty_data['Close'].rolling(window=7).mean()


print(nifty_data[['Date', 'Close', '5-day MA', '7-day MA']])

nifty_data.to_csv('^NSEI.csv')



nifty_data['Slow_MA'] = nifty_data['Close'].rolling(window=7).mean()
nifty_data['Fast_MA'] = nifty_data['Close'].rolling(window=5).mean()

nifty_data['Signal'] = ""
nifty_data.loc[nifty_data['Fast_MA'] > nifty_data['Slow_MA'], 'Signal'] = "buy"
nifty_data.loc[nifty_data['Fast_MA'] < nifty_data['Slow_MA'], 'Signal'] = "sell"

print(nifty_data[['Date', 'Close', 'Fast_MA', 'Slow_MA', 'Signal']])

nifty_data.to_csv('^NSEI.csv', index=False)
