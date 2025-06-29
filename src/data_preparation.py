# This file contains functions for downloading stock data, adding targets, creating features, scaling features, and preparing data for LSTM models.

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.dates import date2num

def download_stock_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    data.dropna(inplace=True)
    return data

def add_target(data: pd.DataFrame) -> pd.DataFrame:
    data['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)
    return data

def create_features(data: pd.DataFrame, sequence_length: int = 60):
    features = []
    targets = []
    for i in range(len(data) - sequence_length):
        features.append(data.iloc[i:i+sequence_length].loc[:, data.columns != 'Target'].values)
        targets.append(data.iloc[i+sequence_length]['Target'])
    return np.array(features), np.array(targets)

def scale_features(data: pd.DataFrame):
    scaler = StandardScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
    return scaled_data, scaler

# The point of this function is to split the data into smaller chunks with a specified length
# this is so the data will be in a format the LSTM model can understand
# the main thing that can be tweeked here is the seq_len, which is just the length of the chunks it wil learn from
def create_lstm_sequences(df, feature_cols, target_col, seq_len=60):
    # select applicable columns
    data = df[feature_cols + [target_col]].values
    X, y = [], []

    # loop over data and create overlapping chunks
    for i in range(len(data) - seq_len):
        # X_seq is all feature columns, excluding target
        # and y_val is just target column
        X_seq = data[i : i + seq_len, :-1] 
        y_val = data[i + seq_len, -1]
        X.append(X_seq)
        y.append(y_val)

    # convert to np array and float32 because of torch
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)
    return X, y
