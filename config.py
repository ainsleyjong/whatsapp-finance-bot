import os
from dotenv import load_dotenv

load_dotenv()

#----- API / URLs -----#
BASE_URL = "https://api.marketaux.com/v1/news/all"
API_KEY = os.getenv("MARKETAUX_KEY")

#----- Query filters -----#
SYMBOLS = "AAPL,MSFT,GOOGL,NVDA,AMZN,TSLA"
INDUSTRIES = "Technology,Industrials,Financial Services"

#----- Runtime defaults -----#
DEFAULT_HOURS = 24
REQUEST_TIMEOUT = 20
SLEEP_BETWEEN_PAGES = 0.5
MAX_PAGES = 3