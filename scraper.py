from requests_html import HTMLSession

class Scraper():
    def scrapedata(self, year, month):
        url = f'https://www.materdei.org/apps/events/{year}/{month}/?id=6'
        s = HTMLSession()
        r = s.get(url)

        eventlist = []

        info = r.html.find('ul.day-event-box')
        date = r.html.find('div.day-date-box')
        item = dict()
        item[year] = dict()

        for i,d in zip(info, date):
            item = {
                d.find('span.date', first=True).text.strip():  i.find('a.event-link', first=True).text.strip()
            }

            eventlist.append(item)



        return eventlist


quotes = Scraper()

quotes.scrapedata('2022', '12')
