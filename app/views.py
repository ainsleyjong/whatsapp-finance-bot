from flask import Blueprint, jsonify, current_app, request 
from flask.typing import ResponseReturnValue
from .utils.whatsapp_utils import get_text_message_input, send_message
import logging

webhook_blueprint = Blueprint("webhook", __name__)

def verify():
    """Required webhook verifictaion for WhatsApp."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    verify_token = current_app.config["WA_VERIFY_TOKEN"]
    
    if mode and token:
        if mode == "subscribe" and token == verify_token:
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

def handle_message():
    """Handle incoming WhatsApp messages."""
    data = request.get_json()
    logging.info(f"Incoming webhook {data}")
    
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        body = message["text"]["body"]
        
        response_data = get_text_message_input(sender, f"Thanks for your message: {body}")
        send_message(response_data)
        
    return jsonify({"status": "success", "message": "message received"}), 200

@webhook_blueprint.route("/", methods=["GET"])
def webhook_test():
    return "Testing 1..2..3!"

@webhook_blueprint.route("/webhook", methods=["GET"]) # type: ignore[arg-type]
def webhook_get():
    return verify()
    
@webhook_blueprint.route("/webhook", methods=["POST"])
def webhook_post():
    return handle_message()