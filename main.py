# main.py

import time
import pandas as pd
from data_collection import fetch_news
from sentiment_analysis import preprocess_text, get_sentiment
from model_training import train_model, predict_stock_movement, fetch_historical_data
from email_notifications import send_email
from stock_price import fetch_current_price

# Define your watchlist
watchlist = ['AAPL', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']

def main():
    # Prepare the historical data and technical indicators for model training
    historical_data = {}
    for stock in watchlist:
        historical_data[stock] = fetch_historical_data(stock)
    
    while True:
        stocks_info = []
        
        for stock in watchlist:
            news_data = fetch_news(stock)
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
                
                features = merged_data[['sentiment_score', 'SMA_20', 'SMA_50', 'RSI', 'Bollinger_Upper', 'Bollinger_Lower']]
                labels = merged_data['Close']
                
                model = train_model(features, labels)
                predicted_prices = predict_stock_movement(model, features)
                
                predicted_price = predicted_prices.mean()  # Use the mean predicted price for simplicity
                current_price = float(fetch_current_price(stock))
                
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
            send_email(stocks_info, 'your_email@example.com')

        # Sleep for a defined period (e.g., 1 hour)
        time.sleep(3600)

if __name__ == "__main__":
    main()









