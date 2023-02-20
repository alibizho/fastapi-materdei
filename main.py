from fastapi import FastAPI
from scraper import Scraper
from helped_scraper import scrapedata


app = FastAPI()

quotes = Scraper()

@app.get('/events')
def read_events(year, month):
    return quotes.scrape_data(year, month)


@app.get('/dresses')
def get_dresses(year, month):
    return quotes.scrape_dress(year,month)
