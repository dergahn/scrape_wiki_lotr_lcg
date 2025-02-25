import requests
from bs4 import BeautifulSoup
import csv

# Base URL to prepend to the links
base_url = "https://hdr-lcg.fandom.com"

# Function to extract german_name (first h1) from a page
def extract_german_name(url):
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first <h1> tag (German name)
        h1_tag = soup.find('h1', {'class': 'page-header__title'})
        
        # If found, return the text
        if h1_tag:
            german_name = h1_tag.get_text(strip=True)
            return german_name
        else:
            return "No h1 found"
    else:
        return f"Failed to retrieve {url}"

# Function to extract german_text (plain text from the next <p> after <h2> with "Kartentext" span)
def extract_german_text(url):
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <h2> tags
        h2_tags = soup.find_all('h2')
        
        for h2 in h2_tags:
            # Skip the <h2> with the text "Inhaltsverzeichnis"
            if "Inhaltsverzeichnis" in h2.get_text(strip=True):
                continue
            
            # Check if the <h2> contains a <span> with the text "Kartentext"
            span_tag = h2.find('span', string="Kartentext")
            if span_tag:
                # Find the next <p> tag after this <h2> tag
                p_tag = h2.find_next('p')
                if p_tag:
                    # Get the plain text from the <p> tag, ignoring any inner tags (like <a>, <b>, etc.)
                    german_text = p_tag.get_text(strip=True)
                    return german_text
        
        return "No relevant <p> found after <h2> with Kartentext"
    else:
        return f"Failed to retrieve {url}"

# URL for the page with the links
url = "https://hdr-lcg.fandom.com/de/wiki/Grundspiel_(Neuauflage)"

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <h4> tags, then find <ul> tags under them
    h4_tags = soup.find_all('h4')
    links = []
    
    for h4 in h4_tags:
        # Find the next <ul> after the <h4>
        ul = h4.find_next('ul')
        if ul:
            # Find all <a> tags within the <ul>
            a_tags = ul.find_all('a')
            for a in a_tags:
                href = a.get('href')
                if href:
                    # Make the link absolute by combining with the base URL
                    full_url = base_url + href
                    links.append(full_url)

    # Create or open a CSV file for writing the data
    with open('german_names_and_text.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'german_name', 'german_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Iterate through the links and extract the german_name and german_text
        for link in links:
            german_name = extract_german_name(link)
            german_text = extract_german_text(link)
            # Write each row of data (URL, German name, and German text) to the CSV
            writer.writerow({'URL': link, 'german_name': german_name, 'german_text': german_text})

    print("Data successfully saved to german_names_and_text.csv")

else:
    print("Failed to retrieve the page")
