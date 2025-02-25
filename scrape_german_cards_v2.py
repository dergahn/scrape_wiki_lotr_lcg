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
    with open('german_names.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'german_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Iterate through the links and extract the german_name
        for link in links:
            german_name = extract_german_name(link)
            # Write each row of data (URL and German name) to the CSV
            writer.writerow({'URL': link, 'german_name': german_name})

    print("Data successfully saved to german_names.csv")

else:
    print("Failed to retrieve the page")
