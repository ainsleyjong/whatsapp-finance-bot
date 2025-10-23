from config import SYMBOLS, INDUSTRIES, MAX_PAGES
from news import extract_data, print_articles

if __name__ == "__main__":
    if SYMBOLS:
        symbol_articles = extract_data(pages=MAX_PAGES, symbols=SYMBOLS)
        print_articles(symbol_articles, header="📈 Articles by SYMBOLS")
        
    if INDUSTRIES:
        industry_articles = extract_data(pages=MAX_PAGES, industries=INDUSTRIES)
        print_articles(industry_articles, header="🏭 Fetching articles by INDUSTRIES")