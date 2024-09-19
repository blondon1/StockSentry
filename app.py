# app.py

import streamlit as st
import pandas as pd
from model_training import fetch_historical_data, train_lstm_model, train_random_forest, predict_stock_movement_lstm, predict_stock_movement_rf, ensemble_prediction
from stock_price import fetch_current_price
from sentiment_analysis import preprocess_text, get_sentiment
from data_collection import fetch_news
from pyspark.sql import SparkSession

# Function to initialize Spark session
def get_spark_session():
    spark = SparkSession.builder \
        .appName("StockPredictionApp") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()
    return spark

# Function to process large datasets with PySpark
def process_large_data_with_spark(data):
    try:
        spark = get_spark_session()

        # Convert Pandas DataFrame to PySpark DataFrame
        df = spark.createDataFrame(data)

        # Example of filtering and aggregation using PySpark
        df_filtered = df.filter(df['close'] > 100)  # Replace 'close' with the actual column name
        df_grouped = df_filtered.groupBy('symbol').agg({'close': 'avg'})  # Example grouping

        # Convert back to Pandas DataFrame
        processed_data = df_grouped.toPandas()

        return processed_data

    except Exception as e:
        st.error(f"Error processing large data: {e}")
        return None

    finally:
        spark.stop()  # Stop Spark session to free up resources

# Sample function to simulate fetching large historical data
def fetch_large_stock_data():
    # This is a placeholder for actual large dataset fetching logic
    data = {
        'symbol': ['AAPL', 'GOOGL', 'NVDA', 'AAPL', 'GOOGL'],
        'close': [150, 250, 500, 160, 300]
    }
    return pd.DataFrame(data)

# Title of the app
st.title("Stock Market Prediction Dashboard")

# User input for stock watchlist
stock_list = st.text_input("Enter stock tickers (comma-separated):", "AAPL,GOOGL,NVDA")
stock_list = [stock.strip() for stock in stock_list.split(",")]

# Prediction interval
interval = st.selectbox("Select prediction interval", ["30 minutes", "1 hour", "4 hours", "1 day"])

# Fetch historical data for each stock and plot closing price chart
if st.button("Fetch Historical Data"):
    for stock in stock_list:
        st.subheader(f"Stock: {stock}")
        data = fetch_historical_data(stock)
        st.line_chart(data['Close'])

# Run prediction using trained models and display predicted prices
if st.button("Run Predictions"):
    for stock in stock_list:
        st.subheader(f"Predictions for {stock}")
        try:
            historical_data = fetch_historical_data(stock)
            features = historical_data[['SMA_20', 'SMA_50', 'RSI', 'ATR', 'Bollinger_Upper', 'Bollinger_Lower']].values
            labels = historical_data['Close'].values

            # Check if we have enough data
            if features.shape[0] == 0:
                st.error(f"Not enough data to make predictions for {stock}")
                continue

            # Train models
            lstm_model = train_lstm_model(features, labels)
            rf_model = train_random_forest(features, labels)
            
            # Make predictions
            lstm_pred = predict_stock_movement_lstm(lstm_model, features)
            rf_pred = predict_stock_movement_rf(rf_model, features)

            # Ensemble prediction
            predicted_prices = ensemble_prediction(lstm_pred, rf_pred)
            
            # Summarize predictions
            min_pred = predicted_prices.min()
            max_pred = predicted_prices.max()
            avg_pred = predicted_prices.mean()

            # Display key prediction results
            st.write(f"Predicted Price Range: ${min_pred:.2f} - ${max_pred:.2f}")
            st.write(f"Average Predicted Price: ${avg_pred:.2f}")
        except Exception as e:
            st.error(f"Error making predictions for {stock}: {e}")

# Fetch live stock prices and display them
if st.button("Fetch Live Prices"):
    for stock in stock_list:
        try:
            current_price = fetch_current_price(stock, "YOUR_ALPHA_VANTAGE_API_KEY")
            st.write(f"Current price of {stock}: ${current_price}")
        except Exception as e:
            st.error(f"Error fetching live price for {stock}: {e}")

# Perform sentiment analysis on news articles and display sentiment scores
if st.button("Run Sentiment Analysis"):
    st.subheader("Sentiment Analysis")
    for stock in stock_list:
        try:
            news_data = fetch_news(stock, "YOUR_NEWS_API_KEY")
            sentiments = []
            for article in news_data['articles']:
                sentiment_score = get_sentiment(preprocess_text(article['description']))
                sentiments.append(sentiment_score['score'])
            st.write(f"Sentiment Score for {stock}: {sentiments}")
        except Exception as e:
            st.error(f"Error fetching sentiment for {stock}: {e}")

