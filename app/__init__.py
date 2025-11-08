from flask import Flask
from app.config import load_configurations, configure_logging
from .views import webhook_blueprint
from .utils.whatsapp_utils import get_text_message_input, send_message
from .utils.scheduler import start_scheduler
import logging

def create_app():
    app = Flask(__name__)
    
    load_configurations(app)
    configure_logging()
    
    # Import and register blueprints
    app.register_blueprint(webhook_blueprint)
    
    # Send a startup message
    with app.app_context():
        try:
            recipient = app.config["WA_RECIPIENT_NUMBER"]
            startup_msg = get_text_message_input(
                recipient,
                "✅ WhatsApp Finance Bot is now online and ready to send financial updates."
            )
            send_message(startup_msg)
            logging.info("Startup WhatsApp message sent successfully.")
        except Exception as e:
            logging.info(f"Failed to send startup message: {e}")
    
    #TODO: Start background scheduler
    start_scheduler(app)
    
    return app