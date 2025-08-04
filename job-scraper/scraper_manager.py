from jjit_scraper import JJITScraper
from nfj_scraper import NFJScraper
from sj_scraper import SJScraper

# TODO: Przetestuj scrapery

class ScraperManager:
    def __init__(self):
        self.scrapers = [
            # NFJScraper(),
            JJITScraper(),
            SJScraper(),
        ]

    def scrape_all(self, max_offers = 10):
        all_offers = []

        for scraper in self.scrapers:
            try:
                scraper.start()
                offers = scraper.scrape(max_offers)
                all_offers.append(offers)

            except Exception as e:
                print(f'[Error]: Failed to scrape data from: {scraper.__class__.__name__}: {str(e)}')
                all_offers.append([])

            finally:
                try:
                    scraper.stop()
                except:
                    pass
        return all_offers


if __name__ == '__main__':
    scraper = ScraperManager()
    print(scraper.scrape_all(20))