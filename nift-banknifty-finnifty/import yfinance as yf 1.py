import yfinance as yf
import pandas as pd
def fetch_yahoo_finance_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
def save_to_csv(data, filename):
    data.to_csv(filename)
if __name__ == "__main__":
    ticker_symbol = "^NSEI"  
    start_date = "2022-07-26"  
    end_date = "2023-07-26"    
    historical_data = fetch_yahoo_finance_data(ticker_symbol, start_date, end_date)
    if historical_data is not None:
        filename = f"{ticker_symbol}_historical_data.csv"
        save_to_csv(historical_data, filename)
        print(f"Data successfully saved to {filename}")