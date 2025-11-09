from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from app.utils.whatsapp_utils import get_text_message_input, send_message
from app.services.market_news import extract_data, build_article_summary
import logging


def send_scheduled_message():
    """Send a scheduled market news update every 24 hours."""
    try:
        recipient = current_app.config["WA_RECIPIENT_NUMBER"]
        industries = current_app.config["MARKET_INDUSTRIES"]
        
        industry_articles = extract_data(pages=1, industries=industries)
        
        #TODO: Modify message to market news
        message = build_article_summary(industry_articles, header="🏭 Fetching articles by INDUSTRIES")
        payload = get_text_message_input(recipient, message)
        send_message(payload)
        logging.info("Recurring message sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send recurring message: {e}")


def start_scheduler(app):
    """Start the background scheduler with Flask context."""
    scheduler = BackgroundScheduler()
    
    def job():
        with app.app_context():
            send_scheduled_message()

    # Run `send_recurring_message` every 5 minutes
    scheduler.add_job(
        func=job,
        trigger="interval",
        minutes=60,
        id="send_scheduled_message",
        replace_existing=True,
    )

    scheduler.start()
    logging.info("🕒 APScheduler started: recurring message every 5 minutes.")
