import requests
import logging
import time

def fetch_with_retry(url, headers, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                delay = 30 * (attempt + 1)  # Exponential backoff
                logging.warning(f"Rate-limited on {url}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Failed to fetch {url} on attempt {attempt + 1}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error with {url}: {e}")
    logging.error(f"Max retries exceeded for {url}. Skipping.")
    return None
