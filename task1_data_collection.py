import requests
import json
import os
import time
from datetime import datetime

# Configuration
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
TARGET_PER_CATEGORY = 25

# Category Keyword Mapping
KEYWORDS = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

def fetch_data():
    # 1. Getting Top 500 Story IDs
    print("Fetching top stories...")
    try:
        id_resp = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        story_ids = id_resp.json()[:500]  # Taking top 500
    except Exception as e:
        print(f"Error fetching IDs: {e}")
        return

    # Storing collected stories for each category in results
    results = {cat: [] for cat in KEYWORDS}
    total_collected = 0

    # 2. Processing stories
    print("Analyzing stories.......")
    for story_id in story_ids:
        # Stop if we've filled 25 stories for every category
        if all(len(stories) >= TARGET_PER_CATEGORY for stories in results.values()):
            break
            
        try:  # Retrieving details for each story using story_id
            item_response = requests.get(f"{BASE_URL}/item/{story_id}.json", headers=HEADERS)
            story = item_response.json()
            
            if not story or 'title' not in story:
                continue
                
            title = story['title']
            title_lower = title.lower()
            
            # Checking keywords against categories
            for category, tags in KEYWORDS.items():
                # If any category has less than required stories
                if len(results[category]) < TARGET_PER_CATEGORY:
                    if any(tag.lower() in title_lower for tag in tags):
                        # Extract and save fields
                        results[category].append({
                            "post_id": story.get("id"),
                            "title": title,
                            "category": category,
                            "score": story.get("score"),
                            "num_comments": story.get("descendants", 0),
                            "author": story.get("by"),
                            "collected_at": datetime.now().strftime("%Y-%m-%d")
                        })
                        total_collected += 1
               # Breaking inner loop to prevent one story being in multiple categories
                        break 
                        
        except Exception as e:
            print(f"Skipping story {story_id} due to error: {e}")
            continue

    # 3. Handle the 2-second sleep per category as mentioned in Task 1
    for category in KEYWORDS.keys():
        print(f"Finalizing {category} category...")
        time.sleep(2)

    # Creating a folder named 'data' if does not exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # 4. Save to a JSON file    
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
    
    # Flatten the dictionary into a single list
    final_output = [item for sublist in results.values() for item in sublist]
    
    with open(filename, 'w') as f:
        json.dump(final_output, f, indent=4)
        
    print(f"Collected {len(final_output)} stories. Saved to {filename}")

if __name__ == "__main__":
    fetch_data()