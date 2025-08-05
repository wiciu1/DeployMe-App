from datetime import datetime, timedelta
from time import sleep

from base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class SJScraper(BaseScraper):
    def get_offer_links(self, max_offers=None):
        experience_levels = ['Junior', 'Staż']
        offers_links = set()

        for experience_level in experience_levels:
            self.fetch_page(f"https://solid.jobs/offers/it;experiences={experience_level}")

            scroll_attempts = 0
            max_scroll_attempts = 5

            while scroll_attempts < max_scroll_attempts and (not max_offers or len(offers_links) < max_offers):
                offers = self.driver.find_elements(By.CSS_SELECTOR, "a.offer")
                new_offers = False

                for offer in offers:
                    href = offer.get_attribute('href')
                    if href:
                        full_url = href
                        if full_url not in offers_links:
                            offers_links.add(full_url)
                            new_offers = True

                            if max_offers and len(offers_links) >= max_offers:
                                break

                if not new_offers:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0

                self.scroll_down()
                sleep(1.5)

        return list(offers_links)[:max_offers] if max_offers else list(offers_links)

    def extract_offer_data(self, offer_url):
        try:
            self.driver.get(offer_url)
            sleep(1.5)

            header = self.wait_for_element("offer-details-header")
            title = header.find_element(By.TAG_NAME, "a").text
            company = header.find_elements(By.XPATH, ".//sj-icon-with-label//span")[0].text
            location = header.find_elements(By.XPATH, ".//sj-icon-with-label//span")[1].text

            try:
                salary = self.wait_for_element("offer-details-salary span.color-dark-grey").text
            except:
                salary = "Nie określono"

            skills_tags = self.driver.find_elements(By.TAG_NAME, "solidjobs-skill-display-advanced")
            skills = {tag.text for tag in skills_tags}

            requirements = self.wait_for_element("offer-details-requirements")
            experience = requirements.find_elements(By.CSS_SELECTOR, "div.badge")[0].text

            return {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "skills": list(skills),
                "experience_level": experience
            }

        except Exception as e:
            print(f"[Error] Extracting SJ offer: {str(e)}")
            return {}

    def cleanup_offer_data(self, offer_data, offer_url):
        cleaned_salary = (offer_data['salary'].replace('\xa0', '').replace('\u2009', ' ')
                         if offer_data.get('salary') else "Nie określono")

        return {
            "site": "SolidJobs",
            "url": offer_url,
            "title": offer_data.get('title', 'Nie określono'),
            "datePosted": datetime.now().strftime('%Y-%m-%d'),
            "validThrough": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            "company": offer_data.get('company', 'Nie określono'),
            "location": offer_data.get('location', 'Nie określono'),
            "experience": offer_data.get('experience_level', 'Nie określono'),
            "salary": cleaned_salary,
            "skills": offer_data.get('skills', ['Nie określono']),
        }