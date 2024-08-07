# email_notifications.py

import requests

def send_email(subject, body, to_email):
    service_id = 'YOUR_SERVICE_ID'
    template_id = 'YOUR_TEMPLATE_ID'
    user_id = 'YOUR_USER_ID'
    
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        'service_id': service_id,
        'template_id': template_id,
        'user_id': user_id,
        'template_params': {
            'subject': subject,
            'body': body,
            'to_email': to_email,
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Email sent successfully")
    else:
        print(f"Failed to send email: {response.text}")

if __name__ == "__main__":
    send_email('Test Subject', 'Test Body', 'recipient@example.com')


