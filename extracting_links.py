from bs4 import BeautifulSoup
import requests
import time
import random 
import json
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO to reduce verbosity
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),  # Log messages to a file
        logging.StreamHandler()  # Also print messages to the console
    ]
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
pages = 563
links = {}
duplicate_links = 0


for page_number in range(1,pages+1):
    
    url_x = f"https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page={page_number}"
    logging.info(f"Fetching page {page_number}: {url_x}")
    
    try: 
        response = requests.get(url_x,headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            logging.warning(f"Rate-limited on page {page_number}. Retrying after 30 seconds.")
            time.sleep(30)  # Longer delay for rate limit
        logging.error(f"Failed to fetch {url_x}: {e}")
        continue
    
    soup = BeautifulSoup(response.text, 'html.parser')
    anchor_tags = soup.select('a.c-finderProductCard_container.g-color-gray80.u-grid')
    
    if not anchor_tags:
        logging.warning(f"No links found on page {page_number}. Total links so far: {len(links)}")
    
    for anchor in anchor_tags:
        href = anchor.get('href')
        if href:
            full_url = f"https://www.metacritic.com{href}"
            if full_url in links:
                duplicate_links += 1
                continue
            links[full_url] = anchor.text.strip()
    if duplicate_links > 0:
        logging.debug(f"Found {duplicate_links} duplicate links on page {page_number}.")

    logging.info(f"Page {page_number} completed. Total links collected: {len(links)}")
    time.sleep(random.uniform(8, 12))

with open('game_links.json', 'w') as f:
    json.dump(links, f, indent=4)

logging.info(f"Scraping completed. Total duplicate links found: {duplicate_links}")