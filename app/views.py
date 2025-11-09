from flask import Blueprint, jsonify, current_app, request 
from flask.typing import ResponseReturnValue
from .utils.whatsapp_utils import is_valid_whatsapp_message, get_whatsapp_status, process_whatsapp_message
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

#TODO: Modify it to be more maintainable
#? Check whatsapp_status and valid_message functions
def handle_message():
    """Handle incoming WhatsApp messages."""
    body = request.get_json()
    
    # Check if it's a WhatsApp status update
    status_update = get_whatsapp_status(body)
    if (status_update):
        status = status_update.get("status")
        recipient = status_update.get("recipient_id")

        logging.info(f"📬 WhatsApp status update: message {status.upper()} to {recipient}")
        return jsonify({"status": "ok"}), 200
    
    if is_valid_whatsapp_message(body):
        process_whatsapp_message(body)
        
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