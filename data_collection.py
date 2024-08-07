# data_collection.py

import requests

def fetch_news(stock):
    api_key = 'YOUR_NEWS_API_KEY'  # Replace with your actual news API key
    url = f'https://newsapi.org/v2/everything?q={stock}&apiKey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    return data

