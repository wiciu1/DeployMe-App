from datetime import datetime, timedelta
import json
from base_scraper import BaseScraper

# TESTED 03.08 | Valid

class JJITScraper(BaseScraper):
    def get_offer_links(self, max_offers=None):
        experience_level_links = {
            'Staż': "https://justjoin.it/job-offers/all-locations?working-hours=practice-internship",
            'Junior': "https://justjoin.it/job-offers/all-locations?experience-level=junior"
        }

        for exp_url in experience_level_links.values():
            self.fetch_page(exp_url)

            # Try to accept cookies
            try:
                self.page.locator("#cookiescript_accept").first.click(timeout=5000)
            except:
                pass

            offers_urls = set()

            # Attempts
            attempts = 0
            max_attempts = 5

            while attempts < max_attempts and (not max_offers or len(offers_urls) < max_offers):
                try:
                    offers = self.page.locator("a.offer-card").all()
                    new_offers_found = False

                    for offer in offers:
                        href = offer.get_attribute("href")
                        if href:
                            full_url = f"https://justjoin.it{href}"
                            if full_url not in offers_urls:
                                offers_urls.add(full_url)
                                new_offers_found = True

                            if max_offers and len(offers_urls) >= max_offers:
                                return list(offers_urls)
                        else:
                            print(f"[Error]: Fetching url: {offer}")

                    # Try to scroll down
                    self.scroll_down(1000)

                    if not new_offers_found:
                        return list(offers_urls)

                except Exception as e:
                    print(f"[Error]: Failed to get offer links: {str(e)}")
                    attempts += 1
                    continue

            return list(offers_urls)

    def extract_offer_data(self, offer_url):
        try:
            self.page.goto(offer_url)

            json_ld = self.page.evaluate('''() => {
                            const script = document.querySelector('script[type="application/ld+json"]');
                            return script ? JSON.parse(script.textContent) : null;
                        }''')


            # data = json.loads(json_ld)

            # Experience level
            # Seniority (Trainee: Junior + Employment Type = Internship)
            #           (Junior: Employment Type != Internship)
            seniority = self.page.locator("div.mui-1ihbss1").nth(1).text_content()
            employment_type = self.page.locator("div.mui-1ihbss1").nth(2).text_content()

            if employment_type == 'Internship':
                exp_level = 'Staż'
            else:
                exp_level = seniority

            json_ld['experience_level'] = exp_level if exp_level else "Nie określono"

            # Salary
            salary_spans = self.page.locator("span.mui-1cfnfqd")
            spans_text = salary_spans.all_text_contents()
            json_ld['salary'] = " - ".join(spans_text) if spans_text else None

            # Skills
            skills_containers = self.page.locator("h4.MuiTypography-root").all()
            skills = []

            for s in skills_containers:
                skill_text = s.text_content()
                skills.append(skill_text)

            json_ld['skills'] = skills
            return json_ld


        except Exception as e:
            print(f"[Error]: Failed to extract offer data: {str(e)}")
            return None

    def cleanup_offer_data(self, data, url):
        if not data:
            return {
                'site': 'JustJoinIT',
                'url': url.split("|")[0] if "|" in url else url,
                'title': 'Nie określono',
                'company': 'Nie określono',
                'experience': 'Nie określono',
                'salary': 'Nie określono',
                'location': 'Nie określono',
                'datePosted': datetime.now().strftime("%Y-%m-%d"),
                'validThrough': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                'skills': ['Nie określono'],
            }

        try:
            clean_url = url.split("|")[0] if "|" in url else url

            date_str = data.get('datePosted')
            date_obj = (
                datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                if date_str
                else datetime.now()
            )
            formatted_date = date_obj.strftime("%Y-%m-%d")

            valid_str = data.get('validThrough')
            valid_obj = (
                datetime.strptime(valid_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                if valid_str
                else (date_obj + timedelta(days=30))
            )
            formatted_valid = valid_obj.strftime("%Y-%m-%d")

            return {
                'site': 'JustJoinIT',
                'url': clean_url,
                'title': data.get('title', 'Nie określono'),
                'company': (data.get('hiringOrganization', {}) or {}).get('name', 'Nie określono'),
                'experience': data.get('experience_level', 'Nie określono'),
                'salary': data.get('salary', 'Nie określono'),
                'location': "Zdalnie" if data.get('jobLocationType') == "TELECOMMUTE"
                else (data.get('jobLocation', {}) or {}).get('address', {}).get('addressLocality', 'Nie określono'),
                'datePosted': formatted_date,
                'validThrough': formatted_valid,
                'skills': data.get('skills', ['Nie określono']),
            }
        except Exception as e:
            print(f"Error cleaning data: {e}")
            return None

    def _format_salary(self, salary_data):
        try:
            min_val = salary_data.get('value', {}).get('minValue')
            max_val = salary_data.get('value', {}).get('maxValue')
            currency = salary_data.get('currency', 'PLN')
            return f"{min_val}-{max_val} {currency}" if min_val and max_val else None
        except:
            return None

if __name__ == "__main__":
    s = JJITScraper()
    print(s.scrape(21))

