from jjit_scraper import JJITScraper
from nfj_scraper import NFJScraper
from sj_scraper import SJScraper
import json


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

    def save_to_json(self, data, filename='offers.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nData saved to {filename}")


if __name__ == '__main__':
    manager = ScraperManager()
    results = manager.scrape_all(5)
    manager.save_to_json(results)

    #
    print("\n=== Summary ===")
    for site, offers in results.items():
        print(f"{site}: {len(offers)} offers")