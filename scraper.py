import feedparser
from deep_translator import GoogleTranslator
import json
from datetime import datetime
import requests

def fetch_all_perspectives():
    print("Starting the multi-source scraper...")
    news_list = []
    translator = GoogleTranslator(source='auto', target='en')
    
    # We must use a custom User-Agent so social media sites don't block our free scraper
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # --- OUR MASTER LIST OF SOURCES ---
    sources = [
        {
            "name": "Jerusalem Post",
            "url": "https://www.jpost.com/rss/rssfeedsfrontpage.aspx",
            "country": "Israel",
            "status": "Verified Media"
        },
        {
            "name": "BBC Persian",
            "url": "https://feeds.bbci.co.uk/persian/rss.xml",
            "country": "Iran",
            "status": "Verified Media"
        },
        {
            "name": "Mehr News Agency",
            "url": "https://en.mehrnews.com/rss",
            "country": "Iran",
            "status": "State-Affiliated Media"
        },
        {
            "name": "Israeli Citizens (Reddit)",
            "url": "https://www.reddit.com/r/Israel/new/.rss",
            "country": "Israel",
            "status": "Unverified / Citizen Voice"
        },
        {
            "name": "Iranian Citizens (Reddit)",
            "url": "https://www.reddit.com/r/NewIran/new/.rss",
            "country": "Iran",
            "status": "Unverified / Citizen Voice"
        }
    ]

    for source in sources:
        print(f"Fetching data from: {source['name']}")
        try:
            # Fetch the data using requests to bypass basic blocks
            response = requests.get(source['url'], headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            # Grab the top 3 most recent posts from EACH source
            for entry in feed.entries[:3]:
                raw_title = entry.title
                
                # We use a trick: if there is no summary, we just use the title again to prevent crashes
                raw_summary = entry.get('summary', 'No summary provided by user.') 
                
                # Translate everything to English just in case it's in Hebrew or Farsi
                english_title = translator.translate(raw_title)
                
                # Clean up the summary (Social media RSS can have messy HTML)
                english_summary = translator.translate(raw_summary[:500]) # Limit to 500 chars for speed
                
                article = {
                    "headline": english_title,
                    "summary": english_summary,
                    "source": source['name'],
                    "country": source['country'],
                    "verification_status": source['status'],  # NEW FIELD!
                    "date": datetime.now().strftime("%B %d, %Y - %H:%M")
                }
                news_list.append(article)
                
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")

    # Save to JSON
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully generated news.json with {len(news_list)} diverse perspectives!")

if __name__ == "__main__":
    fetch_all_perspectives()
