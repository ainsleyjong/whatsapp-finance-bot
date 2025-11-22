# WhatsApp Financial News Automation Bot

This is a Python-based WhatsApp chatbot adapted from the original [python-whatsapp-bot](https://github.com/daveebbelaar/python-whatsapp-bot) that delivers **AI-summarised market news** and responds to **real-time stock symbol queries**, powered by the **WhatsApp Cloud API**, **OpenAI API**, and **MarketAux financial data API**.  
Built with Flask, deployed on AWS EC2 using Gunicorn + Nginx, and includes a daily automated scheduler for pushing market updates.

## Features

- **WhatsApp chatbot** using the official WhatsApp Cloud API
- Fetches live articles from **MarketAux** in the last 24 hours based on:
  - stock symbols (`symbols=META,TSLA`)
  - industries (`industries=Technology,Industrials`)
- Uses **OpenAI GPT-5-mini** to summarise news into a clean WhatsApp-ready message
- Supports **automated daily updates** via APScheduler
- Includes **message template support** for WhatsApp's 24-hour business policy

## Running the Application Locally
1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a `.env` file
```ini
WA_ACCESS_TOKEN=<your_whatsapp_token>
WA_PHONE_NUMBER_ID=<your_phone_number_id>
WA_VERIFY_TOKEN=<your_verify_token>
MARKETAUX_KEY=<your_marketaux_api_key>
OPENAI_API_KEY=<your_openai_key>
```
4. Run locally
```bash
python run.py
```
If testing webhooks locally, expose port 5000 using `ngrok`:
```bash
ngrok http 5000
```

## WhatsApp Capabilities
### Supported Commands
| User Input Example   | Bot Behavior                                                                |
| -------------------- | --------------------------------------------------------------------------- |
| `symbols META`       | Fetches latest META news, summarizes via AI, returns clean WhatsApp message |
| `symbols META TSLA`  | Fetches & summarizes multiple tickers                                       |
| `industries finance` | Returns industry-focused news                                               |
| Other text           | Returns guidance message                                                    |

### Scheduled Updates
- Runs **daily at 12:00 GMT** (configurable)
- Summaries are sent using the **WhatsApp templates** if outside the 24h session window

## Deployment (AWS EC2 Overview)

This project is deployed on EC2 using:
- **Gunicorn** to serve Flask
- **Nginx** as reverse proxy
- **systemd service** for auto-restart + background execution
- Optional: **ngrok systemd service**
