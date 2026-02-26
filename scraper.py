import feedparser
from deep_translator import GoogleTranslator
import json
from datetime import datetime

def fetch_and_translate_news():
    print("Starting the news scraper...")
    
    # 1. The Source: BBC Persian RSS feed
    rss_url = "https://feeds.bbci.co.uk/persian/rss.xml"
    feed = feedparser.parse(rss_url)
    
    news_list = []
    # Set up the free translator (Farsi 'fa' to English 'en')
    translator = GoogleTranslator(source='fa', target='en')
    
    # 2. Loop through the top 5 most recent articles
    for entry in feed.entries[:5]:
        try:
            # Extract the raw Farsi text
            farsi_title = entry.title
            farsi_summary = entry.summary
            
            # Translate to English
            print(f"Translating: {farsi_title}")
            english_title = translator.translate(farsi_title)
            english_summary = translator.translate(farsi_summary)
            
            # 3. Format to match your Android app's NewsArticle data model
            article = {
                "headline": english_title,
                "summary": english_summary,
                "source": "BBC Persian (Auto-Translated)",
                "date": datetime.now().strftime("%B %d, %Y")
            }
            news_list.append(article)
            
        except Exception as e:
            print(f"Error translating an article: {e}")
            
    # 4. Save the formatted data to a JSON file
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)
        
    print("Successfully generated news.json!")

if __name__ == "__main__":
    fetch_and_translate_news()
