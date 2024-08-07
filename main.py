# main.py

import time
import pandas as pd
from data_collection import fetch_news
from sentiment_analysis import preprocess_text, get_sentiment
from model_training import train_model, predict_stock_movement
from email_notifications import send_email

# Define your watchlist
watchlist = ['AAPL', 'GOOGL', 'AMZN', 'TSLA']

def main():
    # Example training data
    features = pd.DataFrame({
        'sentiment_score': [0.1, 0.4, -0.3, 0.2, -0.5],
        'other_feature': [1, 2, 3, 4, 5]
    })
    labels = pd.Series([1, 0, 1, 0, 1])
    
    model = train_model(features, labels)
    
    while True:
        for stock in watchlist:
            news_data = fetch_news(stock)
            sentiment_scores = [get_sentiment(preprocess_text(article['description']))['score'] for article in news_data['articles']]
            
            current_data = pd.DataFrame({'sentiment_score': sentiment_scores, 'other_feature': [3] * len(sentiment_scores)})
            prediction = predict_stock_movement(model, current_data)
            
            predicted_movement = prediction.mean()
            # Assuming a conversion factor to translate sentiment score to dollars for the example
            movement_in_dollars = f"${predicted_movement * 100:.2f}" 
            max_low = min(sentiment_scores)
            max_high = max(sentiment_scores)
            
            send_email(stock, predicted_movement, movement_in_dollars, max_low, max_high, 'your_email@example.com')

        # Sleep for a defined period (e.g., 1 hour)
        time.sleep(3600)

if __name__ == "__main__":
    main()


