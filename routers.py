from fastapi import APIRouter
from my_facebook_scraper import FacebookScraper

router = APIRouter()
facebook_scraper = FacebookScraper()

@router.post("/scrape")  # Changed to POST
async def scrape_facebook_page(request: dict):
    page_url = request.get("page_url")
    data = facebook_scraper.scrape_data(page_url)
    return {"scraped_data": data}
