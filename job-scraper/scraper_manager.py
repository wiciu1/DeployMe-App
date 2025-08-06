from jjit_scraper import JJITScraper
from nfj_scraper import NFJScraper
from sj_scraper import SJScraper

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            NFJScraper(),
            JJITScraper(),
            SJScraper()
        ]

    def scrape_all(self, max_offers_per_site=10):
        results = {}

        for scraper in self.scrapers:
            scraper_name = scraper.__class__.__name__.replace('Scraper', '')
            print(f"\n=== Starting {scraper_name} scraper ===")

            try:
                offers = scraper.scrape(max_offers_per_site)
                results[scraper_name] = offers
                print(f"Successfully scraped {len(offers)} offers from {scraper_name}")
            except Exception as e:
                print(f"[Error] {scraper_name} scraper failed: {str(e)}")
                results[scraper_name] = []

        return results