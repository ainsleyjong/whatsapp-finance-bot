from dotenv import load_dotenv
import json
import os
import requests

#---------- Load Environment Variables ----------#

load_dotenv()
ACCESS_TOKEN = os.getenv("WA_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WA_PHONE_NUMBER_ID")
VERSION = os.getenv("WA_VERSION_ID")
RECIPIENT_NUMBER = os.getenv("WA_RECIPIENT_NUMBER")

#---------- Send a template WhatsApp Message ----------#

def send_template_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_NUMBER,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {"code": "en_US"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Call the function
response = send_template_message()
print(response.status_code)
print(response.json())

#---------- Send a custom WhatsApp message ----------#

def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response

#? Disable to test
data = get_text_message_input(
    recipient=RECIPIENT_NUMBER, text="Hello, this is a test message."
)
response = send_message(data)

