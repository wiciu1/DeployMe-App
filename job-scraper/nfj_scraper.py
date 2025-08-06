from datetime import datetime, timedelta
from time import sleep

from base_scraper import BaseScraper
from selenium.webdriver.common.by import By
import json


class NFJScraper(BaseScraper):
    def get_offer_links(self, max_offers=None):
        self.fetch_page("https://nofluffjobs.com/pl/?criteria=seniority%3Dtrainee,junior")
        offer_urls = set()

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts and (not max_offers or len(offer_urls) < max_offers):
            try:

                offers = self.driver.find_elements(By.CSS_SELECTOR, "a.posting-list-item")

                for offer in offers:
                    href = offer.get_attribute("href")
                    if href:
                        full_url = f'{href}'
                        offer_urls.add(full_url)

                        if max_offers and len(offer_urls) >= max_offers:
                            return list(offer_urls)

                load_more = self.driver.find_elements(By.CSS_SELECTOR, 'button[nfjloadmore]')
                if not load_more:
                    break

                self.driver.execute_script("arguments[0].click();", load_more[0])
                sleep(3)
                attempts = 0

            except Exception as e:
                print(f"[Error] Loading more offers: {str(e)}")
                attempts += 1
                sleep(2)

        return list(offer_urls)[:max_offers] if max_offers else list(offer_urls)

    def extract_offer_data(self, offer_url):
        try:
            self.driver.get(offer_url)
            script_element = self.driver.find_element(By.CSS_SELECTOR, 'script[type="application/ld+json"]')
            json_data = json.loads(script_element.get_attribute('textContent'))

            job_posting = next(
                (item for item in json_data["@graph"] if item.get("@type") == "JobPosting"),
                None
            )

            if not job_posting:
                return None

            date_posted = job_posting.get("datePosted")
            valid_through = job_posting.get("validThrough")

            if date_posted:
                try:
                    date_posted_obj = datetime.strptime(date_posted, "%Y-%m-%d")
                    if valid_through is None:
                        valid_through_obj = date_posted_obj + timedelta(days=30)
                        valid_through = valid_through_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass

            result = {
                "title": job_posting.get("title", "Nie określono"),
                "company": job_posting.get("hiringOrganization", {}).get("name", "Nie określono"),
                "experience": job_posting.get("experienceRequirements", {}).get("description", "Nie określono"),
                "datePosted": job_posting.get("datePosted", "Nie określono"),
                "validThrough": valid_through or "Nie określono",
                "location": "Zdalnie" if job_posting.get("jobLocationType") == "TELECOMMUTE"
                else job_posting.get("jobLocation", {}).get("address", {}).get("addressLocality", "Nie określono"),
                "salary": None,
                "skills": []
            }

            salary_data = job_posting.get("baseSalary", {})
            if salary_data:
                value = salary_data.get("value", {}).get("value")
                currency = salary_data.get("currency", "PLN")
                unit = salary_data.get("value", {}).get("unitText", "month")
                if value:
                    result["salary"] = f"{value} {currency}/{unit}"
            else:
                result['salary'] = "Nie określono"

            skills = job_posting.get("skills", [])
            if skills:
                result["skills"] = [skill.get("value") for skill in skills if skill.get("value")]

            if result["experience"] == 'Trainee':
                result["experience"] = 'Staż'

            return result

        except Exception as e:
            print(f"[Error] Extracting data from {offer_url}: {str(e)}")
            return None

    def cleanup_offer_data(self, offer_data, offer_url):
            offer_data['site'] = 'NoFluffJobs'
            offer_data['url'] = offer_url
            return offer_data