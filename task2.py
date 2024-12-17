import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def retrieve_website_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
        cleaned_text = ' '.join([para.get_text(strip=True) for para in paragraphs])
        return cleaned_text
    except requests.exceptions.SSLError as ssl_error:
        logging.error(f"SSL error occurred: {ssl_error}")
    except requests.exceptions.RequestException as request_error:
        logging.error(f"Request error occurred: {request_error}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def search_for_content(query, data_store):
    found_matches = []
    for url, content in data_store.items():
        if query.lower() in content.lower():
            found_matches.append((url, content))
    return found_matches

def run_scraper():
    urls_to_scrape = [
        "https://www.uchicago.edu/",
        "https://www.washington.edu/",
        "https://www.stanford.edu/",
        "https://und.edu/"
    ]

    scraped_content = {}
    for url in urls_to_scrape:
        content = retrieve_website_data(url)
        if content:
            logging.info(f"Successfully retrieved content from {url}")
            scraped_content[url] = content

    user_query = input("Enter your query: ")
    results = search_for_content(user_query, scraped_content)

    if results:
        print("\nResults found:")
        for url, content in results:
            print(f"\nFrom {url}:\n{content[:500]}...")
    else:
        print("No results found for your query.")

    print("\nYou can navigate to the following links:")
    print(f"{Colors.RED}- {urls_to_scrape[0]}{Colors.RESET}")
    print(f"{Colors.GREEN}- {urls_to_scrape[1]}{Colors.RESET}")
    print(f"{Colors.BLUE}- {urls_to_scrape[2]}{Colors.RESET}")

if __name__ == "__main__":
    run_scraper()
