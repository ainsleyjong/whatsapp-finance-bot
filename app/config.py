from dotenv import load_dotenv
import os
import logging
import sys

def load_configurations(app):
    load_dotenv()

    #---------- WhatsApp Credentials ----------#
    app.config["WA_ACCESS_TOKEN"] = os.getenv("WA_ACCESS_TOKEN")
    app.config["WA_PHONE_NUMBER_ID"] = os.getenv("WA_PHONE_NUMBER_ID")
    app.config["WA_BUSINESS_ACCOUNT_ID"] = os.getenv("WA_BUSINESS_ACCOUNT_ID")
    app.config["WA_VERSION_ID"] = os.getenv("WA_VERSION_ID")
    app.config["WA_RECIPIENT_NUMBER"] = os.getenv("WA_RECIPIENT_NUMBER")
    app.config["WA_VERIFY_TOKEN"] = os.getenv("WA_VERIFY_TOKEN")

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )