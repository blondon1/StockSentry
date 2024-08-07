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
            
            for article in news_data['articles']:
                description = article.get('description')
                if description:
                    preprocessed_text = preprocess_text(description)
                    sentiment_score = get_sentiment(preprocessed_text)['score']
                    sentiment_scores.append(sentiment_score)
            
            if sentiment_scores:
                current_data = pd.DataFrame({'sentiment_score': sentiment_scores})
                historical = historical_data[stock].iloc[-1]
                current_data['SMA_20'] = historical['SMA_20']
                current_data['SMA_50'] = historical['SMA_50']
                current_data['RSI'] = historical['RSI']
                current_data['Bollinger_Upper'] = historical['Bollinger_Upper']
                current_data['Bollinger_Lower'] = historical['Bollinger_Lower']
                
                model = train_model(current_data, historical_data[stock]['Close'])
                prediction = predict_stock_movement(model, current_data)
                
                predicted_movement = prediction.mean()
                movement_in_dollars = f"${predicted_movement * 100:.2f}" 
                max_low = min(sentiment_scores)
                max_high = max(sentiment_scores)
                current_price = fetch_current_price(stock)
                
                stocks_info.append({
                    'stock': stock,
                    'current_price': f"${float(current_price):.2f}",
                    'predicted_movement': f"{predicted_movement:.2f}",
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






