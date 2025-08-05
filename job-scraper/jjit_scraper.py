import json
from datetime import datetime, timedelta
from time import sleep

from base_scraper import BaseScraper
from selenium.webdriver.common.by import By


class JJITScraper(BaseScraper):
    def get_offer_links(self, max_offers=None):
        experience_level_links = {
            'Staż': "https://justjoin.it/job-offers/all-locations?working-hours=practice-internship",
            'Junior': "https://justjoin.it/job-offers/all-locations?experience-level=junior"
        }

        offers_urls = set()

        for exp_level, exp_url in experience_level_links.items():
            self.fetch_page(exp_url)

            try:
                self.wait_for_element("#cookiescript_accept").click()
            except:
                pass

            attempts = 0
            max_attempts = 3

            while attempts < max_attempts and (not max_offers or len(offers_urls) < max_offers):
                offers = self.driver.find_elements(By.CSS_SELECTOR, "a.offer-card")
                new_offers = False

                for offer in offers:
                    href = offer.get_attribute("href")
                    if href:
                        full_url = href
                        if full_url not in offers_urls:
                            offers_urls.add(full_url)
                            new_offers = True

                            if max_offers and len(offers_urls) >= max_offers:
                                break

                if not new_offers or (max_offers and len(offers_urls) >= max_offers):
                    break

                self.scroll_down()
                attempts += 1
                sleep(2)

        return list(offers_urls)[:max_offers] if max_offers else list(offers_urls)

    def extract_offer_data(self, offer_url):

        def format_date(date_str):
            try:
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
            except:
                return date_str

        try:
            self.driver.get(offer_url)
            self.wait_for_element("div.mui-1ihbss1", timeout=15)

            script_element = self.driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
            json_data = json.loads(script_element.get_attribute('textContent'))

            # Experience
            titles = self.driver.find_elements(By.CSS_SELECTOR, "div.mui-1ihbss1")
            type_of_work = titles[0].text
            if type_of_work == 'Practice / Internship':
                experience_level = 'Staż'
            else:
                experience_level = titles[1].text

            # Salary
            salary = self.driver.find_element(By.CSS_SELECTOR, "span.mui-1fhatg7").text
            if salary == 'Undisclosed Salary':
                salary = 'Nie określono'

            # Skills
            skills = self.driver.find_elements(By.CSS_SELECTOR, "h4.MuiTypography-root")
            skills_tag = []
            for skill in skills:
                skills_tag.append(skill.text)

            job_data = {
                "title": json_data.get("title", "Nie określono"),
                "company": json_data.get("hiringOrganization", {}).get("name", "Nie określono"),
                "experience": experience_level,
                "salary": salary,
                "location": json_data.get("jobLocation", {}).get("address", {}).get("addressLocality", "Nie określono"),
                "datePosted": format_date(json_data.get("datePosted", "")),
                "validThrough": format_date(json_data.get("validThrough", "")),
                "skills": skills_tag
            }

            return job_data

        except Exception as e:
            print(f"[Error] Failed to extract offer data from {offer_url}: {str(e)}")
            return None

    def cleanup_offer_data(self, data, url):
        data['site'] = 'JustJoinIT'
        data['url'] = url
        return data