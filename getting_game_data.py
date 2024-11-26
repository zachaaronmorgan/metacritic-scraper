import json
import requests
from bs4 import BeautifulSoup
import logging
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO to reduce verbosity
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),  # Log messages to a file
        logging.StreamHandler()  # Also print messages to the console
    ]
)

# Load links from scraped data
with open('game_links.json', 'r') as f:
    links = json.load(f).keys()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

game_info = {}

for link in links:
    logging.info(f"Fetching link: {link}")
    try: 
        response = requests.get(link, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            logging.warning(f"Rate-limited on page: {link}. Retrying after 30 seconds.")
            time.sleep(30)  # Longer delay for rate limit
        logging.error(f"Failed to fetch {link}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract game title
    title_tag = soup.select_one('div[data-testid="hero-title"] h1')
    title = title_tag.text.strip() if title_tag else "Unknown Title"

    # Extract platforms
    platform_tags = soup.select('a.c-gamePlatformTileLink[href*="platform="]')
    platforms = [tag['href'].split("platform=")[-1] for tag in platform_tags]  # Extract platform names

    # Extract release date
    release_date_tag = soup.select_one('div.g-text-xsmall span.u-text-uppercase')
    release_date = release_date_tag.text.strip() if release_date_tag else "Unknown Release Date"

    # Extract genres (replace the selector with the correct one for genres)
    # Extract genres
    genre_tags = soup.select('ul.c-genreList li a span.c-globalButton_label')
    genres = [tag.text.strip() for tag in genre_tags]

    # Extract Metascore
    metascore_tag = soup.select_one('div.c-siteReviewScore_background-critic_medium span')
    metascore = metascore_tag.text.strip() if metascore_tag else "Unknown Score"

    # Extract User Score
    user_score_tag = soup.select_one('div.c-siteReviewScore_background-user span')
    user_score = user_score_tag.text.strip() if user_score_tag else "Unknown Score"

    # Add game info to dictionary
    game_info[title] = {
        "platforms": platforms,
        "release_date": release_date,
        "genres": genres,
        "metacritic_score": metascore,
        "user_score": user_score
    }


    logging.info(f"Added data for: {title}")

    # Random delay to avoid being rate-limited
    time.sleep(random.uniform(5, 10))

# Save the game_info dictionary to a file
with open('game_info.json', 'w') as f:
    json.dump(game_info, f, indent=4)

logging.info("Scraping completed.")