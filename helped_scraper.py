import asyncio
import requests_async as req
from bs4 import BeautifulSoup
from itertools import zip_longest
from requests_html import HTMLSession
import requests

table_info = []

async def fetchLink(link):
    global table_info
    
    href = link.attrs['href']
    burl = f'https://www.materdei.org{href}'

    b = await req.get(burl, verify=False)


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
            xx = x.get_text(separator='   ').strip()
            table_info.append(xx)


async def getInfo(i):
    links = i.find('a.event-link')

    await asyncio.gather(*[asyncio.create_task(fetchLink(link)) for link in links], return_exceptions=False)


async def get_tables(info):
    global table_info

    await asyncio.gather(*[asyncio.create_task(getInfo(i)) for i in info], return_exceptions=False)

    return table_info
    

def scrapedata(year, month):
    url = f'https://www.materdei.org/apps/events/{year}/{month}/?id=6'

    s = HTMLSession()
    r = s.get(url)

    info = r.html.find('ul.day-event-box')
    date = r.html.find('div.day-date-box')

    tables = asyncio.run(get_tables(info))



    eventlist = []

    for i, d, t in zip_longest(info, date, tables, fillvalue='There is no table for this event!'):
        try:
            item = {
                'Day': d.find('span.date', first=True).text.strip(),
                'Block': i.find('a.event-link', first=True).text.strip(),
                'Table': t,
                'Month': month,
                'Year': year,
            }
            eventlist.append(item)
        except TypeError:
            print("FUCK ME")

    return eventlist

