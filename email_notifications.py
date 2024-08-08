# email_notifications.py

import requests

def send_email(stocks_info, to_email, config):
    service_id = config['email_service_id']
    template_id = config['email_template_id']
    user_id = config['email_user_id']
    private_key = config['email_private_key']
    
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

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

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
    config = {
        'email_service_id': 'your_service_id',
        'email_template_id': 'your_template_id',
        'email_user_id': 'your_user_id',
        'email_private_key': 'your_private_key',
        'email_to': 'recipient@example.com'
    }
    send_email(stocks_info, config['email_to'], config)
