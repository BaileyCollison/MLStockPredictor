import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
import data_preparation as dp
import matplotlib.figure as Figure


def plot_price_and_volume(ticker):
    df = dp.download_stock_data(ticker, start_date='2020-01-01', end_date='2023-10-01')
    dates   = date2num(df.index.to_pydatetime())
    close   = df['Close'].astype(float).values
    volume  = df['Volume'].astype(float).values

    # Flatten volume if it's 2D
    if volume.ndim > 1:
        volume = volume.flatten()

    # Ensure same length
    min_len = min(len(dates), len(volume))
    dates = dates[:min_len]
    close = close[:min_len]
    volume = volume[:min_len]

    fig = Figure.Figure(figsize=(14, 6))
    ax1 = fig.add_subplot(111)
    ax1.set_title(f"{ticker} – Close & Volume")
    ax1.plot(df.index[:min_len], close)
    ax1.set_ylabel('Close')
    ax1.grid(True)

    ax2 = ax1.twinx()
    ax2.bar(dates, volume,
            width=1.0,
            alpha=0.3,
            linewidth=0,
            edgecolor='none')
    ax2.set_ylabel('Volume')
    ax2.xaxis_date()

    fig.tight_layout()
    plt.show()

    return fig  # Return the figure object if needed for further processing
