from datetime import timedelta, datetime
from time import sleep

from base_scraper import BaseScraper

# TODO: Nie extractuje danych, gdy musi scrollować

class NFJScraper(BaseScraper):

    def get_offer_links(self, max_offers=None):
        self.fetch_page("https://nofluffjobs.com/pl/?criteria=seniority%3Dtrainee,junior")

        offer_urls = set()
        self.page.wait_for_selector("a.posting-list-item", timeout=10000)

        # Attempts:
        attempts = 0
        max_attempts = 5

        while attempts < max_attempts and (not max_offers or len(offer_urls) < max_offers):
            try:
                self.page.wait_for_selector("a.posting-list-item", timeout=10000)
                offers = self.page.locator("a.posting-list-item")
                offers_count = offers.count()

                print(f"Znaleziono {offers_count} ofert na stronie")

                for i in range(offers_count):
                    offer = offers.nth(i)
                    href = offer.get_attribute("href")
                    if href:
                        full_url = f'https://nofluffjobs.com{href}'
                        if full_url not in offer_urls:
                            offer_urls.add(full_url)
                            print(f"Dodano ofertę {len(offer_urls)}: {full_url}")

                            if max_offers and len(offer_urls) >= max_offers:
                                return list(offer_urls)

                    else:
                        print(f"[Warning]: Error fetching href from {offer}")

                # Handle loading more offers
                load_more_button = self.page.locator('button[nfjloadmore]')

                # There are no offers left
                if load_more_button.count() == 0:
                    print("[Info]: No more offers to load")
                    break


                # Click the button
                try:
                    load_more_button.scroll_into_view_if_needed()
                    self.page.wait_for_timeout(1000)
                    sleep(2)

                    self.page.evaluate('''(selector) => {
                                            document.querySelector(selector).click();
                                        }''', 'button[nfjloadmore]')

                    self.page.wait_for_timeout(2000)

                    previous_count = offers_count
                    try:
                        self.page.wait_for_function(
                            f"document.querySelectorAll('a.posting-list-item').length > {previous_count}",
                            timeout=10000
                        )
                    except:
                        print("Nowe oferty nie zostały załadowane")

                    attempts = 0

                except Exception as e:
                    print(f"[Error]: Failed to click load more: {str(e)}")
                    attempts += 1
                    continue

            except Exception as e:
                print(f"[Error]: Failed to get offer links: {str(e)}")
                attempts += 1
                continue

        return list(offer_urls)

    def extract_offer_data(self, offer_url):
        try:
            self.page.goto(offer_url, timeout=15000)
            self.page.wait_for_timeout(2000)

            json_data = self.page.locator("script[type='application/json']").text_content()

            if not json_data:
                print(f"[Warning]: Brak danych JSON dla {offer_url}")
                return None

            return json_data


        except Exception as e:
            print(f"[Error extracting {offer_url}]: {e}")
            return None

    def cleanup_offer_data(self, offer_data, offer_url):
        try:
            job_offer = next(
                (item for item in offer_data.get("@graph", []) if item.get("@type") == 'JobPosting'), {}
            )

            base_salary = job_offer.get("baseSalary", {})
            currency = base_salary.get("currency", "PLN")
            amount = base_salary.get("value", {}).get("value", "0")
            unit = base_salary.get("value", {}).get("unitText", "month")
            skills_list = job_offer.get("skills", [])

            date_str = job_offer.get("datePosted")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.now()
            normalized_date = date_obj.strftime("%Y-%m-%d")

            valid_through_raw = job_offer.get("validThrough")
            valid_through_obj = (datetime.strptime(valid_through_raw, "%Y-%m-%d")) if valid_through_raw else (
                        date_obj + timedelta(days=30))
            valid_through_final = valid_through_obj.strftime("%Y-%m-%d")

            experience_level = (job_offer.get("experienceRequirements") or {}).get("description", "Nie określono")

            if experience_level == 'Junior':
                experience_level = 'Junior'
            elif experience_level == 'Trainee':
                experience_level = 'Staż'

            return {
                'site': 'NoFluffJobs',
                'url': offer_url,
                'title': job_offer.get('title', 'Nie określono'),
                "datePosted": normalized_date,
                "validThrough": valid_through_final,
                "company": (job_offer.get("hiringOrganization") or {}).get("name", "Nie określono"),
                "location": "Zdalnie" if job_offer.get("JobLocationType") == "TELECOMMUTE"
                else (job_offer.get("jobLocation") or {}).get("address", {}).get("addressLocality", "Nie określono"),
                'experience': experience_level,
                'salary': f"{amount} {currency} / {unit}" if amount and currency and unit else "Nie określono",
                'skills': [skill.get("value") for skill in skills_list if skill.get("value")] or ["Nie określono"],
            }
        except Exception as e:
            print(f"Error cleaning data for {offer_url}: {str(e)}")
            return None


if __name__ == "__main__":
    s = NFJScraper()
    print(s.scrape(2))

