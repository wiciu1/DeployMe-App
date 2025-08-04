from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright
from time import sleep

# BaseScraper - abstract class of other scrapers
# Has methods that are used by child classes (for specific site)

class BaseScraper(ABC):
    def __init__(self):
        self.page = None
        self.browser = None

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def stop(self):
        self.browser.close()
        self.playwright.stop()

    # Method to scrape all offers from one site
    def scrape(self, max_offers = None):

        self.start()

        # Get all offers links
        offers_urls = self.get_offer_links(max_offers)

        cleaned_data = []

        for offer_url in offers_urls:
            # Extract data
            print(f"Extract data from: {offer_url}")
            extracted_data = self.extract_offer_data(offer_url)
            if extracted_data:
                # Clean data
                print(extracted_data)
                cleaned_data.append( self.cleanup_offer_data(extracted_data, offer_url) )
            else:
                print(f"[Warning]: No data extracted for {offer_url}")

        self.stop()
        return cleaned_data

    def fetch_page(self, url):
        try:
            self.page.goto(url, timeout=30000)
            return self.page.content()
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            return None

    def scroll_down(self, step = 500):
        previous_height = 0

        while True:
            self.page.evaluate(f'window.scrollBy(0, {step})')
            sleep(1.5)

            new_height = self.page.evaluate("document.body.scrollHeight")

            # If height didn't change (nothing more)
            if new_height == previous_height:
                break

            previous_height = new_height

    # Abstract methods

    @abstractmethod
    def extract_offer_data(self, offer_url):
        pass

    @abstractmethod
    def cleanup_offer_data(self, offer_data, offer_url):
        pass

    # Gets link for specific offer
    @abstractmethod
    def get_offer_links(self, max_offers = None):
        pass

