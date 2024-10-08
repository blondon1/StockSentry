# stock_price.py

import requests

def fetch_current_price(stock, api_key):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'Global Quote' in data and '05. price' in data['Global Quote']:
        return data['Global Quote']['05. price']
    else:
        print(f"Error fetching price for {stock}: {data}")
        return None
