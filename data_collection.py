# data_collection.py

import requests

def fetch_news(stock):
    api_key = 'YOUR_NEWS_API_KEY'
    url = f'https://newsapi.org/v2/everything?q={stock}&apiKey={api_key}'
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    watchlist = ['AAPL', 'GOOGL', 'AMZN', 'TSLA']
    for stock in watchlist:
        print(fetch_news(stock))
