from flask import current_app, jsonify
import json
import logging
import requests

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get("content-type")}")
    logging.info(f"Body: {response.text}")

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
        "Authorization": f"Bearer {current_app.config["WA_ACCESS_TOKEN"]}"
    }
    
    url = f"https://graph.facebook.com/{current_app.config["WA_VERSION_ID"]}/{current_app.config["WA_PHONE_NUMBER_ID"]}/messages"
    
    try:
        response = requests.post(
            url=url, data=data, headers=headers, timeout=10
        )
        response.raise_for_status()
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (requests.RequestException) as e:
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    
    