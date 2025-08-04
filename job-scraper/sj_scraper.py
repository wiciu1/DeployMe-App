import time
from datetime import datetime, timedelta

from base_scraper import BaseScraper

# TESTED 03.08 | Valid


class SJScraper(BaseScraper):   
    def extract_offer_data(self, offer_url):
        self.page.goto(offer_url)
        time.sleep(1.5)

        try:
            # Header
            offer_header = self.page.locator("offer-details-header")
            title = offer_header.locator("a").first.text_content()
            company = offer_header.locator('//sj-icon-with-label//span').nth(0).text_content()
            location = offer_header.locator('//sj-icon-with-label//span').nth(1).text_content()

            # Salary
            offer_salary = self.page.locator("offer-details-salary")
            try:
                salary = offer_salary.locator("span.color-dark-grey").nth(0).text_content()
            except:
                salary = "0"

            # Requirements
            offer_requirements = self.page.locator("offer-details-requirements")
            skills_tags = self.page.locator("solidjobs-skill-display-advanced").all()
            skills = set()
            for skill in skills_tags:
                skill_text = skill.text_content()
                skills.add(skill_text)

            experience_level = offer_requirements.locator("div.badge").nth(0).text_content()

            data = {
                "title": title,
                "company": company,
                "location": location,
                "salary": salary,
                "skills": list(skills),
                "experience_level": experience_level
            }

            return data

        except Exception as e:
            print(f"[Error]: {e}")
            return {}

    def cleanup_offer_data(self, offer_data, offer_url):
        cleaned_salary = (
            offer_data['salary'].replace('\xa0', '').replace('\u2009', ' ')
            if offer_data.get('salary')
            else "Nie określono"
        )

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

    def get_offer_links(self, max_offers=None):
        experience_levels = ['Junior', 'Staż']
        offers_links = set()

        for experience_level in experience_levels:
            self.fetch_page(f"https://solid.jobs/offers/it;experiences={experience_level}")

            previous_count = 0
            no_new_offers_scrolls = 0
            max_scroll_attempts = 5

            while True:
                offers = self.page.locator("a.offer").all()
                new_offers_found = False

                for offer in offers:
                    href = offer.get_attribute('href')
                    if href:
                        full_url = f'https://solid.jobs{href}'
                        if full_url not in offers_links:
                            offers_links.add(full_url)
                            new_offers_found = True

                            if max_offers and len(offers_links) >= max_offers:
                                break

                if max_offers and len(offers_links) >= max_offers:
                    break

                if not new_offers_found:
                    no_new_offers_scrolls += 1
                    if no_new_offers_scrolls >= max_scroll_attempts:
                        print(f"[{experience_level}] no new offers after {max_scroll_attempts} scrolls.")
                        break
                else:
                    no_new_offers_scrolls = 0

                self.scroll_down(1000)
                time.sleep(1.5)

        return list(offers_links)

if __name__ == "__main__":
    s = SJScraper()
    print(s.scrape(41))