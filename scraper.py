from requests_html import HTMLSession
import json
from bs4 import BeautifulSoup
import requests
from itertools import zip_longest
import re

class Scraper():
    def scrapedata(self, year, month):
        url = f'https://www.materdei.org/apps/events/{year}/{month}/?id=6'

        s = HTMLSession()
        r = s.get(url)

        eventlist = []

        info = r.html.find('ul.day-event-box')
        date = r.html.find('div.day-date-box')


        # TABLE RETURN
        def get_tables():

            table_info = []


            for i in info:
                links = i.find('a.event-link')

                for link in links:
                    href = link.attrs['href']

                    burl = f'https://www.materdei.org{href}'

                    b = requests.get(burl)

                    soup = BeautifulSoup(b.content, 'html.parser')

                    try:
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
                                xx = x.get_text(separator='   ').strip()
                                table_info.append(xx)

                    except AttributeError:
                        table_info.append("There is no table for this event!")
            return table_info


        item = dict()
        item[year] = dict()

        tables = get_tables()

        for i, d, t in zip_longest(info, date, tables, fillvalue='There is no table for this event!'):


            item = {
                'Day': d.find('span.date', first=True).text.strip(),
                'Block': i.find('a.event-link', first=True).text.strip(),
                'Table': t,
                'Month': month,
                'Year': year,
            }
            eventlist.append(item)

        return eventlist


quotes = Scraper()

quotes.scrapedata(2023,1)

