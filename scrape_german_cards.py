import requests
from bs4 import BeautifulSoup
import csv
import time

# Define the function first
def scrape_card_details(card_url):
    """Scrape detailed information from an individual card page."""
    response = requests.get(card_url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract card text
        card_text = ""
        card_text_section = soup.find("h2", string="Kartentext")  # Look for the "Kartentext" section
        if card_text_section:
            card_text = card_text_section.find_next("div").get_text(strip=True)

        # Extract information from the infobox (e.g., Type, Sphere, Position, Traits, Keywords)
        infobox = soup.find("table", class_="portable-infobox")
        sphere_name = ""
        position = ""
        traits = ""
        keywords = ""
        type_name = ""

        if infobox:
            # Extract "Karten Art" (Type)
            type_section = infobox.find("th", string="Karten Art")
            if type_section:
                type_name = type_section.find_next("td").get_text(strip=True)

            # Extract "Sphäre" (Sphere)
            sphere_section = infobox.find("th", string="Sphäre")
            if sphere_section:
                sphere_name = sphere_section.find_next("td").get_text(strip=True)

            # Extract "Karten-Nummer" (Position)
            position_section = infobox.find("th", string="Karten-Nummer")
            if position_section:
                position = position_section.find_next("td").get_text(strip=True)

            # Extract "Merkmale" (Traits)
            traits_section = infobox.find("th", string="Merkmale")
            if traits_section:
                traits = traits_section.find_next("td").get_text(strip=True)

            # Extract "Schlüssel-Wörter" (Keywords)
            keywords_section = infobox.find("th", string="Schlüssel-Wörter")
            if keywords_section:
                keywords = keywords_section.find_next("td").get_text(strip=True)

        return [sphere_name, position, traits, keywords, card_text]

    else:
        print(f"❌ Failed to fetch card page: {card_url}")
        return None


# URL of the German card set
URL = "https://hdr-lcg.fandom.com/de/wiki/Grundspiel_(Neuauflage)"
OUTPUT_CSV = "german_cards_full_data.csv"

# Send a GET request to the page
response = requests.get(URL)

# Check if the page was fetched successfully
if response.status_code == 200:
    print("✅ Page fetched successfully!")

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the h4 tags (each represents a card type like "Helden", "Verbündete")
    card_types = soup.find_all("h4")

    # Prepare a list to store card details
    cards = []

    # Loop through each card type section (e.g., "Helden", "Verbündete")
    for card_type in card_types:
        type_name = card_type.get_text(strip=True)

        # Find the corresponding <ul> with links to the cards
        card_list = card_type.find_next("ul")

        if card_list:
            # Find all the links (<a>) within the <ul> that represent individual cards
            card_links = card_list.find_all("a")

            # Iterate over the links and extract the card names and URLs
            for link in card_links:
                card_name = link.get_text(strip=True)
                card_url = link.get("href")  # URL to the individual card page
                if not card_url.startswith("http"):
                    card_url = "https://hdr-lcg.fandom.com" + card_url  # Fix relative URLs

                # Scrape details from the individual card page
                card_details = scrape_card_details(card_url)

                # Add the card data to the list
