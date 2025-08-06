from typing import List, Optional
import uvicorn
from fastapi import FastAPI, Path, HTTPException

from api.JobOffer import JobOffer
from scraper_manager import ScraperManager

app = FastAPI(
    title="Job Scraper API",
    description="API getting offers data from NoFluffJobs, JustJoinIT, SolidJobs"
)


@app.get("/offers", response_model=List[JobOffer], summary="Get job offers (query params version)")
async def get_offers_query(max_offers: int = 100, site: Optional[str] = None):
    """
    Gets job offers from given sites using query parameters.

    - **max_offers**: Maximum offers to load (default: 100)
    - **site**: Site filter [optional] (e.g. 'justjoinit', 'nofluffjobs', 'solidjobs')
    """
    return await _fetch_offers(max_offers, site)


@app.get("/offers/{max_offers}", response_model=List[JobOffer], summary="Get job offers (path param version)")
async def get_offers_path(
        max_offers: int = Path(..., gt=0, le=200, description="Maximum offers to load"),
        site: Optional[str] = None
):
    """
    Gets job offers from given sites using path parameter.

    - **max_offers**: Maximum offers to load (required, 1-200)
    - **site**: Site filter [optional] (e.g. 'justjoinit', 'nofluffjobs', 'solidjobs')
    """
    return await _fetch_offers(max_offers, site)


async def _fetch_offers(max_offers: int, site: Optional[str] = None):
    """Shared function to fetch offers"""
    try:
        scraper = ScraperManager()
        results = scraper.scrape_all(max_offers)

        all_offers = []
        for portal_offers in results.values():
            all_offers.extend(portal_offers)

        if site:
            all_offers = [offer for offer in all_offers if site.lower() in offer['site'].lower()]

        return all_offers[:max_offers]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

