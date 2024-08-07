# email_notifications.py

import requests

def send_email(stock, predicted_movement, movement_in_dollars, max_low, max_high, to_email):
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
            'stock': stock,
            'predicted_movement': predicted_movement,
            'movement_in_dollars': movement_in_dollars,
            'max_low': max_low,
            'max_high': max_high,
            'to_email': to_email,
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print(f"Failed to send email: {response.text}")

if __name__ == "__main__":
    send_email('AAPL', 0.35, '$35.00', -0.5, 0.9, 'recipient@example.com')




