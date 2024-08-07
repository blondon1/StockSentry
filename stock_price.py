# stock_price.py

import requests

def fetch_current_price(stock):
    api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your Alpha Vantage API key
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    if 'Global Quote' in data:
        return data['Global Quote']['05. price']
    else:
        print(f"Error fetching price for {stock}: {data}")
        return "N/A"
