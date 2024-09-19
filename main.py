# main.py

import time
import pandas as pd
import os
from data_collection import fetch_news
from sentiment_analysis import preprocess_text, get_sentiment
from model_training import train_lstm_model, train_random_forest, predict_stock_movement_lstm, predict_stock_movement_rf, fetch_historical_data, ensemble_prediction
from email_notifications import send_email
from stock_price import fetch_current_price
from crypto_utils import generate_key, load_key, save_key, save_config, load_config
import numpy as np

def get_user_input():
    api_key = input("Enter your Alpha Vantage API key: ")
    news_api_key = input("Enter your News API key: ")
    email_service_id = input("Enter your EmailJS service ID: ")
    email_template_id = input("Enter your EmailJS template ID: ")
    email_user_id = input("Enter your EmailJS user ID: ")
    email_private_key = input("Enter your EmailJS private key: ")
    email_to = input("Enter your email address to receive updates: ")
    watchlist = input("Enter the five stocks for your watchlist (comma-separated): ").split(',')
    
    return {
        "alpha_vantage_api_key": api_key,
        "news_api_key": news_api_key,
        "email_service_id": email_service_id,
        "email_template_id": email_template_id,
        "email_user_id": email_user_id,
        "email_private_key": email_private_key,
        "email_to": email_to,
        "watchlist": [stock.strip() for stock in watchlist]
    }

def main():
    if os.path.exists("config.enc"):
        use_existing = input("Configuration file found. Do you want to use the current configuration? (yes/no): ").lower()
        if use_existing == 'yes':
            key = load_key()
            config = load_config(key)
        else:
            config = get_user_input()
            key = generate_key()
            save_key(key)
            save_config(config, key)
    else:
        config = get_user_input()
        key = generate_key()
        save_key(key)
        save_config(config, key)

    watchlist = config['watchlist']
    
    # Prepare the historical data and technical indicators for model training
    historical_data = {}
    for stock in watchlist:
        historical_data[stock] = fetch_historical_data(stock)
    
    while True:
        stocks_info = []
        
        for stock in watchlist:
            news_data = fetch_news(stock, config['news_api_key'])
            sentiment_scores = []
            dates = []
            
            for article in news_data['articles']:
                description = article.get('description')
                if description:
                    preprocessed_text = preprocess_text(description)
                    sentiment_score = get_sentiment(preprocessed_text)['score']
                    sentiment_scores.append(sentiment_score)
                    dates.append(article['publishedAt'][:10])  # Assuming the date is in 'publishedAt'
            
            if sentiment_scores:
                current_data = pd.DataFrame({'date': dates, 'sentiment_score': sentiment_scores})
                current_data['date'] = pd.to_datetime(current_data['date'])
                
                historical = historical_data[stock]
                historical['Date'] = pd.to_datetime(historical['Date'])
                
                # Align sentiment scores with historical data
                merged_data = pd.merge(current_data, historical, left_on='date', right_on='Date', how='inner')
                
                features = merged_data[['sentiment_score', 'SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']].values
                labels = merged_data['Close'].values
                
                # Train both LSTM and RandomForest models
                lstm_model = train_lstm_model(features, labels)
                rf_model = train_random_forest(features, labels)
                
                # Predict stock movement using both models
                lstm_pred = predict_stock_movement_lstm(lstm_model, features)
                rf_pred = predict_stock_movement_rf(rf_model, features)
                
                # Get the ensemble prediction
                predicted_prices = ensemble_prediction(lstm_pred, rf_pred)
                
                predicted_price = predicted_prices.mean()  # Use the mean predicted price for simplicity
                current_price = fetch_current_price(stock, config['alpha_vantage_api_key'])
                
                if current_price is None:
                    continue  # Skip this stock if current price could not be fetched
                
                current_price = float(current_price)
                
                # Calculate movement in dollars as the difference between current price and predicted price
                movement_in_dollars = f"${predicted_price - current_price:.2f}" 
                max_low = min(sentiment_scores)
                max_high = max(sentiment_scores)
                
                stocks_info.append({
                    'stock': stock,
                    'current_price': f"${current_price:.2f}",
                    'predicted_movement': f"${predicted_price:.2f}",
                    'movement_in_dollars': movement_in_dollars,
                    'max_low': f"{max_low:.2f}",
                    'max_high': f"{max_high:.2f}"
                })
        
        if stocks_info:
            send_email(stocks_info, config['email_to'], config)

        # Sleep for a defined period (e.g., 1 hour)
        time.sleep(3600)

if __name__ == "__main__":
    main()
