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
OUTPUT_CSV = "cards_data_with_german.csv"  # Output file with empty German fields

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

# Step 5: Save to CSV with empty fields for German translations
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    # Write the header with empty fields for German translations
    writer.writerow([
        "name", "type_name", "sphere_name", "position", "traits", "keywords", "text", "flavor", 
        "shadow", "german_name", "german_type_name", "german_sphere_name", "german_position", 
        "german_traits", "german_keywords", "german_text", "german_flavor", "german_shadow"
    ])  # Header with empty columns for German translations

    # Write the card data and empty fields for German translation
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
            "",  # Empty field for German name
            "",  # Empty field for German type_name
            "",  # Empty field for German sphere_name
            "",  # Empty field for German position
            "",  # Empty field for German traits
            "",  # Empty field for German keywords
            "",  # Empty field for German text
            "",  # Empty field for German flavor
            "",  # Empty field for German shadow
        ])

print(f"✅ Saved {len(filtered_cards)} cards with empty German fields to {OUTPUT_CSV}!")
