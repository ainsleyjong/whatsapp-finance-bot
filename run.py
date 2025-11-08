from app import create_app
import logging

app = create_app()

if __name__ == "__main__":
    logging.info("Flask app started")
    
    #* Run the Flask development server
    #  host="0.0.0.0" → makes the app accessible from any network interface (not just localhost)
    #  port=5000 → default Flask port
    #  When testing webhooks (e.g., WhatsApp), you can expose this server to the internet using ngrok:
    #      ngrok http 5000
    app.run(host="0.0.0.0", port=5000)