import feedparser
import json
import os
import hashlib
from datetime import datetime
#from openai import OpenAI 万一以后有钱可以用这个功能呢
#from summary import summarize_podcast

RSS_FEEDS = [
    {
        "name": "RFI",
        "url": "https://www.rfi.fr/fr/podcasts/rss"
    },
    {
        "name": "France Inter",
        "url": "https://www.radiofrance.fr/franceinter/rss"
    },
    {
        "name": "France Culture",
        "url": "https://www.radiofrance.fr/franceculture/rss"
    }
]

OUTPUT_FILE = os.path.join(
    os.path.dirname(__file__), "../data/podcasts.json"
    )

MAX_ITEMS=100

def fetch_podcasts(source):
    feed = feedparser.parse(source["url"])
    podcasts = []
    
    for entry in feed.entries[:10]:
        title = entry.get("title", "No Title")
        link = entry.get("link", "") 
        published = entry.get("published", "")
        
        audio_url = None
        
        for enclosure in entry.get("enclosures", []):
            href = enclosure.get("href")
            if href:
                audio_url = href
                break 

        if not audio_url:
            for link in entry.get("links", []):
                if "audio" in link.get("type", ""):
                    audio_url = link.get("href")
                    break

        if not audio_url:
            continue
        
        podcast_id=hashlib.md5(audio_url.encode()).hexdigest()
        
        #summary = generate_summary(title)
        
        podcasts.append({
            "id": podcast_id,
            "source": source["name"],
            "title": title,
            "link": link,
            "audio_url": audio_url,
            "published": published,
            "fetched_at": datetime.now().isoformat()
            #"summary": summary
        })
        
    return podcasts

def load_existing():
    if not os.path.exists(OUTPUT_FILE):
        return []
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
    
def remove_duplicates(podcasts):
    unique={}
    
    for podcast in podcasts:
        if podcast["audio_url"] not in unique:
            unique[podcast["audio_url"]] = podcast
    return list(unique.values())



      
def main():
    all_podcasts = load_existing()
    
    for source in RSS_FEEDS:
        new_podcasts = fetch_podcasts(source)
        all_podcasts.extend(new_podcasts)
        
    all_podcasts = remove_duplicates(all_podcasts)
    
    all_podcasts.sort(
        key=lambda x: x["published"],
        reverse=True
    )
    all_podcasts = all_podcasts[:MAX_ITEMS]
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_podcasts, f, ensure_ascii=False, indent=2)
    print("unpdated")

        
if __name__ == "__main__":
    main()