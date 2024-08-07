# main.py

import time
import pandas as pd
from data_collection import fetch_news
from sentiment_analysis import preprocess_text, get_sentiment
from model_training import train_model, predict_stock_movement
from email_notifications import send_email
from stock_price import fetch_current_price  # Import the function from stock_price.py

# Define your watchlist
watchlist = ['AAPL', 'GOOGL', 'AMZN', 'TSLA', 'MSFT']

def main():
    # Example training data
    features = pd.DataFrame({
        'sentiment_score': [0.1, 0.4, -0.3, 0.2, -0.5],
        'other_feature': [1, 2, 3, 4, 5]
    })
    labels = pd.Series([1, 0, 1, 0, 1])
    
    model = train_model(features, labels)
    
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
                current_data = pd.DataFrame({'sentiment_score': sentiment_scores, 'other_feature': [3] * len(sentiment_scores)})
                prediction = predict_stock_movement(model, current_data)
                
                predicted_movement = prediction.mean()
                # Assuming a conversion factor to translate sentiment score to dollars for the example
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





