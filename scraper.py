import feedparser
import json
from datetime import datetime
import requests
from deep_translator import GoogleTranslator
import time

def fetch_massive_news():
    print("Starting the massive multi-source scraper...")
    news_list = []
    
    # Standard headers to bypass blocks
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    # --- THE AGGREGATOR LINKS ---
    # These two Google News links automatically pull from HUNDREDS of verified publishers
    sources = [
        {
            "name": "Google News Aggregator (Israel)",
            "url": "https://news.google.com/rss/search?q=Israel+when:1d&hl=en-US&gl=US&ceid=US:en",
            "country": "Israel",
            "status": "Verified Media",
            "needs_translation": False
        },
        {
            "name": "Google News Aggregator (Iran)",
            "url": "https://news.google.com/rss/search?q=Iran+when:1d&hl=en-US&gl=US&ceid=US:en",
            "country": "Iran",
            "status": "Verified Media",
            "needs_translation": False
        },
        {
            "name": "Iranian Citizens (Reddit)",
            "url": "https://www.reddit.com/r/NewIran/new/.rss",
            "country": "Iran",
            "status": "Unverified / Citizen Voice",
            "needs_translation": True
        }
    ]

    translator = GoogleTranslator(source='auto', target='en')

    for source in sources:
        print(f"Fetching from: {source['name']}")
        try:
            response = requests.get(source['url'], headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            # We will grab the top 15 stories from each aggregator (45 total per run)
            for entry in feed.entries[:15]:
                raw_title = entry.title
                raw_summary = entry.get('summary', 'No summary provided.')
                
                # Google News puts the actual publisher name in the 'source' tag
                actual_publisher = entry.get('source', {}).get('title', source['name'])

                # Only translate if it's the citizen/local sources to prevent getting blocked
                if source['needs_translation']:
                    title = translator.translate(raw_title)
                    summary = translator.translate(raw_summary[:300])
                    time.sleep(1) # Pause for 1 second so we don't get banned by the free translator
                else:
                    title = raw_title
                    summary = raw_summary

                article = {
                    "headline": title,
                    "summary": summary,
                    "source": actual_publisher,  # This will now say "Reuters", "Al Jazeera", etc.
                    "country": source['country'],
                    "verification_status": source['status'],
                    "date": datetime.now().strftime("%B %d, %Y - %H:%M")
                }
                news_list.append(article)
                
        except Exception as e:
            print(f"Error fetching {source['name']}: {e}")

    # Save to JSON
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully generated news.json with {len(news_list)} articles from hundreds of global sources!")

if __name__ == "__main__":
    fetch_massive_news()
