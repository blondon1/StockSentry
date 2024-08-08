# data_collection.py

import requests

def fetch_news(stock, api_key):
    url = f'https://newsapi.org/v2/everything?q={stock}&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data


