from fastapi import FastAPI
from scraper import Scraper
from pydantic import BaseModel

app = FastAPI()

quotes = Scraper()


@app.get('/events')
async def read_events(year, month):
    return quotes.scrapedata(year, month)
