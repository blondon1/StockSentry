# email_notifications.py

import requests

def send_email(stocks_info, to_email):
    service_id = 'YOUR_SERVICE_ID'
    template_id = 'YOUR_TEMPLATE_ID'
    user_id = 'YOUR_USER_ID'
    private_key = 'YOUR_PRIVATE_KEY'
    
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'service_id': service_id,
        'template_id': template_id,
        'user_id': user_id,
        'accessToken': private_key,
        'template_params': {
            'to_email': to_email,
            'stocks': stocks_info
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print(f"Failed to send email: {response.text}")

if __name__ == "__main__":
    stocks_info = [
        {
            'stock': 'AAPL',
            'current_price': '$150.00',
            'predicted_movement': '0.35',
            'movement_in_dollars': '$35.00',
            'max_low': '-0.5',
            'max_high': '0.9'
        }
    ]
    send_email(stocks_info, 'recipient@example.com')






