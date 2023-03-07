from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from itertools import zip_longest
import re


class Scraper():

    def scrape_data(self, year, month):
        url = f'https://www.materdei.org/apps/events/{year}/{month}/?id=6'

        b = requests.get(url)

        soup = BeautifulSoup(b.content, 'html.parser')

        info = soup.findAll('ul', class_='day-event-box')
        date = soup.findAll('span', class_='date')


        def get_tables():

            table_info = []


            for i in info:
                links = i.findAll('a', class_='event-link')

                for link in links:
                    href = link.attrs['href']

                    burl = f'https://www.materdei.org{href}'

                    b = requests.get(burl)

                    soup = BeautifulSoup(b.content, 'html.parser')

                    table = soup.find('table', class_='MsoNormalTable')
                    semester = soup.find('p', class_='MsoNormal')
                    no_school_event_info = soup.findAll('div', class_='event-info')
                    for no in no_school_event_info:
                        no_school = no.find('dd').get_text().strip()
                        if no_school[0:9] == 'No School':
                            table_info.append('There is no table for this event!')

                    if table:
                        dable = soup.findAll('p', class_='MsoNormal')
                        texts = []
                        for text in dable:
                            texts.append(text.text)
                        table_info.append(texts)
                    elif semester:
                        event_info = soup.findAll('div', class_='event-info')
                        for me in event_info:
                            x = me.find('p')
                            xx = x.get_text(separator='  ')
                            words = re.split(r'\s{2,}', xx)
                            table_info.append(words)


            return table_info




        tables = get_tables()
        eventlist = []


        for i, d, t in zip_longest(info, date, tables, fillvalue='There is nothing'):
            try:
                item = {
                    'Date': d if d == str(d) else d.get_text().strip(),
                    'Block': i.find('a', class_='event-link').get_text().strip(),
                    'Table': t,
                    'Month': month,
                    'Year': year
                }

                eventlist.append(item)
            except TypeError:
                print("fail")

        return eventlist


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
