from flask import current_app, jsonify
from app.services.marketaux_service import extract_data, format_articles_for_summary
from app.services.openai_service import summarise_articles_text
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
    
def is_valid_whatsapp_message(body):
    """Check if the incoming webhook event is a valid WhatsApp message."""
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
    
def get_whatsapp_status(body):
    """
    Extract WhatsApp status update from webhook body if present.
    Returns the first status object or None if not a status update.
    """
    try:
        value = body["entry"][0]["changes"][0]["value"]
        if "statuses" in value and value["statuses"]:
            return value["statuses"][0]
    except (KeyError, IndexError, TypeError):
        pass
    return None

def generate_response(message_body):
    text = message_body.strip()

    if text.lower().startswith("symbols"):
        rest = text[len("symbols"):].strip()

        #* Allow formats like:
        #   symbols=META
        #   symbols META
        #   symbols: META,TSLA
        while rest and rest[0] in ["=", ":", " "]:
            rest = rest[1:].strip()

        if not rest:
            return (
                "⚠️ No symbol provided.\n\n"
                "Try using *symbols=<ticker>* — for example:\n"
                "`symbols=META` or `symbols=TSLA,NVDA`"
            )

        # Ensure symbols are comma-separated for Marketaux query
        symbols = rest.upper().replace(" ", ",")

        try:
            articles = extract_data(pages=1, symbols=symbols)
        except Exception as e:
            logging.exception("Error fetching Marketaux data")
            return "⚠️ I couldn't fetch market news right now. Please try again later."

        if not articles:
            return f"No recent news found for symbols=*{symbols}*."

        raw_text = format_articles_for_summary(articles, header=f"📈 Latest news for *{symbols}*")
        summary = summarise_articles_text(raw_text=raw_text)
        return summary
    else:
        return ("⚠️ Command unavailable.\n\n"
            "Try using *symbols <your text>* — for example:\n"
            "`symbols=META`")
    

def process_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    sender = message["from"]
    message_body = message["text"]["body"]
    
    logging.info(f"💬 Incoming WhatsApp message from {sender}: {message_body}")
    
    response = generate_response(message_body)
    response_data = get_text_message_input(sender, response)
    send_message(response_data)