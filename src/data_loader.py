import yfinance as yf
import pandas as pd

def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.dropna(inplace=True)
    return data
