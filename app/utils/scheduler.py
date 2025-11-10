from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from app.utils.whatsapp_utils import get_text_message_input, send_message
from app.services.marketaux_service import extract_data, format_articles_for_summary
from app.services.openai_service import summarise_articles_text
from pytz import timezone
import logging


def send_scheduled_message():
    """Send a scheduled market news update every 24 hours."""
    try:
        recipient = current_app.config["WA_RECIPIENT_NUMBER"]
        industries = current_app.config["MARKET_INDUSTRIES"]
        
        industry_articles = extract_data(pages=3, industries=industries)
        raw_text = format_articles_for_summary(industry_articles, header="🏭 Fetching articles by INDUSTRIES")
        summary = summarise_articles_text(raw_text=raw_text)
        
        payload = get_text_message_input(recipient, summary)
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

    # Run `send_scheduled_message` everyday at 12pm
    scheduler.add_job(
        func=job,
        trigger="cron",
        hour=12,
        minute=0,
        id="send_scheduled_message",
        replace_existing=True,
        timezone=timezone("Europe/London"),
    )

    scheduler.start()
    tz = timezone("Europe/London")
    logging.info(f"🕒 APScheduler started: recurring message scheduled daily at 12:00 PM GMT.{tz}")
