# model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import yfinance as yf
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np

def calculate_technical_indicators(df):
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['Close'])
    df['ATR'] = calculate_atr(df)
    df['Bollinger_Upper'] = df['SMA_20'] + 2 * df['Close'].rolling(window=20).std()
    df['Bollinger_Lower'] = df['SMA_20'] - 2 * df['Close'].rolling(window=20).std()
    
    # Drop rows with missing values
    df = df.dropna()
    
    return df

def calculate_rsi(series, period=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_atr(df, period=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(window=period).mean()

def fetch_historical_data(stock):
    df = yf.download(stock, period='1y')
    df = calculate_technical_indicators(df)
    df.reset_index(inplace=True)
    return df

# LSTM Model for Time-Series Prediction
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm_model(X_train, y_train):
    # Check if X_train has enough data points
    if X_train.shape[0] == 0:
        raise ValueError("Insufficient data for training")
    
    # Reshape the data for LSTM model
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))  # Reshape for LSTM
    lstm_model = build_lstm_model((X_train.shape[1], 1))
    lstm_model.fit(X_train, y_train, batch_size=1, epochs=3)
    return lstm_model

def train_random_forest(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    return rf_model

# Predict function for LSTM model
def predict_stock_movement_lstm(model, features):
    features = np.reshape(features, (features.shape[0], features.shape[1], 1))
    return model.predict(features)

# Predict function for Random Forest model
def predict_stock_movement_rf(model, features):
    return model.predict(features)

# Ensemble Prediction combining LSTM and Random Forest
def ensemble_prediction(lstm_pred, rf_pred):
    return (lstm_pred + rf_pred) / 2
