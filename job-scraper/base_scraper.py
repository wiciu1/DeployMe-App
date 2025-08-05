from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json


class BaseScraper(ABC):
    def __init__(self):
        self.driver = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--false')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')

    def start(self):
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.implicitly_wait(10)

    def stop(self):
        if self.driver:
            self.driver.quit()

    def scrape(self, max_offers=None):
        self.start()
        offers_urls = self.get_offer_links(max_offers)
        cleaned_data = []

        for offer_url in offers_urls[:max_offers] if max_offers else offers_urls:
            print(f"Extracting data from: {offer_url}")
            extracted_data = self.extract_offer_data(offer_url)
            if extracted_data:
                cleaned = self.cleanup_offer_data(extracted_data, offer_url)
                if cleaned:
                    cleaned_data.append(cleaned)
            else:
                print(f"[Warning] No data extracted for {offer_url}")

        self.stop()
        return cleaned_data

    def fetch_page(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
            return None

    def scroll_down(self, step=500):
        current_height = 0
        while True:
            new_height = self.driver.execute_script(
                f"window.scrollTo(0, {current_height}); return document.body.scrollHeight;")
            if new_height == current_height:
                break
            current_height = new_height
            sleep(1.5)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, selector)))

    def parse_json_ld(self):
        try:
            script = self.wait_for_element('script[type="application/ld+json"]')
            return json.loads(script.get_attribute('textContent'))
        except:
            return None

    @abstractmethod
    def extract_offer_data(self, offer_url):
        pass

    @abstractmethod
    def cleanup_offer_data(self, offer_data, offer_url):
        pass

    @abstractmethod
    def get_offer_links(self, max_offers=None):
        pass