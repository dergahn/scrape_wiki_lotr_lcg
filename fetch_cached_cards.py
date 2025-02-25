import requests
import json
import os
import time
import csv

# Step 1: Define constants
CACHE_FILE = "cached_cards.json"  # Cached file
CACHE_EXPIRY = 24 * 60 * 60  # 24 hours
JSON_URL = "https://hallofbeorn.com/Export/AleP"
SET_NAME = "Revised Core Set"  # Change this to any set you want
OUTPUT_CSV = "cards_data_coreset_eng.csv"  # Output file

# Step 2: Check if cache exists and is valid
def is_cache_valid():
    if os.path.exists(CACHE_FILE):
        file_age = time.time() - os.path.getmtime(CACHE_FILE)
        return file_age < CACHE_EXPIRY
    return False

# Step 3: Load data from cache or download
if is_cache_valid():
    print("✅ Using cached data.")
    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        card_data = json.load(file)
else:
    print("🌍 Downloading fresh data...")
    response = requests.get(JSON_URL)
    if response.status_code == 200:
        card_data = response.json()
        with open(CACHE_FILE, "w", encoding="utf-8") as file:
            json.dump(card_data, file, indent=4)
        print("✅ Data cached successfully.")
    else:
        print("❌ Failed to download JSON. Exiting.")
        exit()

# Step 4: Filter cards by set (now using "pack_name")
filtered_cards = [card for card in card_data if card.get("pack_name") == SET_NAME]

# Step 5: Save to CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "type_name", "sphere_name", "position", "traits", "keywords", "text", "flavor", "shadow"])  # Header

    for card in filtered_cards:
        writer.writerow([
            card.get("name", "Unknown"),
            card.get("type_name", "Unknown"),
            card.get("sphere_name", "Unknown"),
            card.get("position", "Unknown"),
            card.get("traits", "None"),
            card.get("keywords", "None"),
            card.get("text", "None"),
            card.get("flavor", "None"),
            card.get("shadow", "None"),
        ])

print(f"✅ Saved {len(filtered_cards)} cards to {OUTPUT_CSV}!")
