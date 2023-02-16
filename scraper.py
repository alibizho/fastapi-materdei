from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests

class Scraper():

    def scrape_dress(self,year, month):

        url = f'https://www.materdei.org/apps/events/{year}/{month}/?id=27'

        s = HTMLSession()
        r = s.get(url)


        eventlist = []




        b = requests.get(url)

        soup = BeautifulSoup(b.content, 'html.parser')

        dresses = soup.body.find_all('a',class_="event-link" )
        for d in dresses:
            if "Dress" in d.get('aria-label'):
                item = {
                    'Date': d.get('aria-label').split("-",1)[0].strip(),
                    'Event': d.get('aria-label')[11:].strip()
                }
                eventlist.append(item)

        return eventlist
