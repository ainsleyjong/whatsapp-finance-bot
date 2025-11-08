from app.services.market_news import extract_data, print_articles

SYMBOLS = "AAPL,MSFT,GOOGL,NVDA,AMZN,TSLA"
INDUSTRIES = "Technology,Industrials,Financial Services"

if __name__ == "__main__":
    if SYMBOLS:
        symbol_articles = extract_data(pages=1, symbols=SYMBOLS)
        print_articles(symbol_articles, header="📈 Articles by SYMBOLS")
        
    if INDUSTRIES:
        industry_articles = extract_data(pages=1, industries=INDUSTRIES)
        print_articles(industry_articles, header="🏭 Fetching articles by INDUSTRIES")