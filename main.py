from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional
from scraper import Scraper
from storage import JSONStorage
from notifier import ConsoleNotifier
from cache import Cache
import uvicorn
import os
from dotenv import load_dotenv


load_dotenv()
STATIC_TOKEN = os.getenv("STATIC_TOKEN")
print(f"STATIC_TOKEN: {STATIC_TOKEN}")

app = FastAPI()

def authenticate(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")

class ScrapeSettings(BaseModel):
    page_limit: Optional[int] = Field(None, ge=1, description="Number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")

@app.post("/scrape")
def scrape(settings: ScrapeSettings, auth: str = Depends(authenticate)):
    storage = JSONStorage()
    notifier = ConsoleNotifier()
    cache = Cache()
    scraper = Scraper(storage=storage, notifier=notifier, cache=cache, settings=settings)

    scraped_count = scraper.run()

    notifier.notify(f"Scraping completed. {scraped_count} products were scraped and updated.")

    return {"detail": "Scraping completed"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


