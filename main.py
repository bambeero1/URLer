import json
import logging
import sys
import argparse
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
from colorlog import ColoredFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the default level to DEBUG

# Add a console handler for real-time display of log messages on the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Set to DEBUG for real-time display of log messages

# Use colorlog's ColoredFormatter for colored logs
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s:%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def save_to_json(all_urls, website_hostname, main_url, negative_save):
    try:
        updated_urls = []

        for url in all_urls:
            parsed_url = urlparse(url)

            # Skip URL if it contains any negative_save keyword
            if any(keyword in url for keyword in negative_save):
                logger.debug(f"Skipping URL due to negative_save keyword: {url}")
                continue

            # Append domain name if not present in the URL
            if not parsed_url.netloc:
                updated_url = urljoin(main_url, url)
                updated_urls.append(updated_url)
            else:
                updated_urls.append(url)

        json_data = {
            "website_hostname": website_hostname,
            "all_urls": updated_urls
        }

        file_name = f"{website_hostname}.json"
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=2)

        num_urls = len(json_data["all_urls"])
        logger.info(f"Saved {num_urls} URLs to {file_name}.")

    except Exception as e:
        logger.error(f"Error saving to JSON: {e}")

def save_to_txt(all_urls, website_hostname, main_url, negative_save):
    try:
        updated_urls = []

        for url in all_urls:
            parsed_url = urlparse(url)

            # Skip URL if it contains any negative_save keyword
            if any(keyword in url for keyword in negative_save):
                logger.debug(f"Skipping URL due to negative_save keyword: {url}")
                continue

            # Append domain name if not present in the URL
            if not parsed_url.netloc:
                updated_url = urljoin(main_url, url)
                updated_urls.append(updated_url)
            else:
                updated_urls.append(url)

        file_name = f"{website_hostname}.txt"
        with open(file_name, 'w', encoding='utf-8') as txt_file:
            for url in updated_urls:
                txt_file.write(url + '\n')

        num_urls = len(updated_urls)
        logger.info(f"Saved {num_urls} URLs to {file_name}.")

    except Exception as e:
        logger.error(f"Error saving to TXT: {e}")

def get_links(page_url, website_hostname, page, main_url, output_format, negative_crawl, negative_save, last_visited_urls):
    global all_urls, counter

    try:
        page.goto(urljoin(main_url, page_url))

        # Extract all hrefs from the current page
        hrefs = page.query_selector_all('a[href]') or []

        for link in hrefs:
            href = link.get_attribute('href')
            full_url = urljoin(main_url, href)

            # Skip URL if it contains any negative_crawl keyword
            if any(keyword in full_url for keyword in negative_crawl):
                continue

            # Skip URL if it has been visited in the last 24 hours
            if full_url in last_visited_urls and datetime.now() - last_visited_urls[full_url] < timedelta(days=1):
                continue

            # Treat hrefs as URLs and add them to the all_urls set
            logger.debug(f"Found href: {full_url}")  # Change to DEBUG level
            all_urls.add(full_url)

        # Process URLs
        for url in all_urls:
            new_page = urlparse(url).path

            if new_page not in all_urls:
                logger.debug(f"Found new URL: {new_page}")  # Change to DEBUG level
                all_urls.add(new_page)
                counter += 1

                # Update last visited time for the URL
                last_visited_urls[url] = datetime.now()

                if counter % 10 == 0:
                    if output_format == 'json':
                        save_to_json(all_urls, website_hostname, main_url, negative_save)
                    else:
                        save_to_txt(all_urls, website_hostname, main_url, negative_save)

                # Log crawling progress in the specified format
                if logger.getEffectiveLevel() == logging.INFO:
                    logger.info(f"Crawling page {counter}: Unique urls: {len(all_urls)} in queue urls: {len(all_urls) - counter}")

                get_links(new_page, website_hostname, page, main_url, output_format, negative_crawl, negative_save, last_visited_urls)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def main(main_url, output_format, negative_crawl, negative_save):
    global all_urls, counter

    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()

        try:
            parsed_url = urlparse(main_url)
            website_hostname = parsed_url.hostname
            logger.info(f"Starting web scraping for {main_url}\n{'='*40}")

            # Set to store all URLs
            all_urls = set()

            # Dictionary to store the last visited time for each URL
            last_visited_urls = {}

            get_links("", website_hostname, page, main_url, output_format, negative_crawl, negative_save, last_visited_urls)

        finally:
            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Scraping Script")
    parser.add_argument("main_url", help="Main URL to start scraping")
    parser.add_argument("-o", "--output", choices=["json", "txt"], default="txt", help="Output format (json or txt)")
    parser.add_argument("--negative_crawl", nargs='+', default=[], help="Keywords to skip crawling if found in URL")
    parser.add_argument("--negative_save", nargs='+', default=[], help="Keywords to skip saving if found in URL")
    parser.add_argument("--log-level", choices=["debug", "info"], default="info", help="Logging level (debug or info)")

    args = parser.parse_args()

    main_url = args.main_url
    output_format = args.output
    negative_crawl = args.negative_crawl
    negative_save = args.negative_save

    # Set the logging level based on the command-line argument
    log_level = logging.DEBUG if args.log_level == "debug" else logging.INFO
    logger.setLevel(log_level)

    counter = 0

    main(main_url, output_format, negative_crawl, negative_save)
