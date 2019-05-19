import json
from lxml import html
from random import shuffle
import requests
from time import ctime

class Odds:

    def __init__(self):
        self.races = {}


    def race_links(self, race=None):
        r = requests.get(
            'https://www.oddschecker.com/horse-racing',
            headers={'User-Agent': 'Mozilla/5.0'}
        )

        if r.status_code == 200:
            doc = html.fromstring(r.content)

            races = doc.xpath('//div[@class="module show-times"]')[0].xpath('.//div[@class="racing-time"]/a')

            return ['https://www.oddschecker.com' + race.attrib['href'] for race in races]
        else:
            return []


    def runner_info(self, runner):
        info = {}
        info["name"] = runner.attrib['data-bname']
        info["draw"] = runner.attrib['data-stall']
        info["number"] = runner.xpath('.//td[@class="cardnum"]/text()')[0]
        try:
            info["jockey"] = runner.xpath('.//div[@class="bottom-row jockey"]/text()')[0]
        except:
            info["jockey"] = ''
        try:
            info['form'] = runner.xpath('.//span[@class="current-form"]/text()')[0]
        except:
            info['form'] = ''
        info['odds'] = {}

        return info


    def load_race(self, link):
        race = []
        r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})

        if r.status_code == 200:
            doc = html.fromstring(r.content)
            runners = doc.xpath('//tbody[@id="t1"]')[0].xpath('.//tr')

            for runner in runners:
                info = self.runner_info(runner)
                prices = runner.xpath('.//td[@data-odig]')

                try:
                    prices = [prices[i] for i in [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 15]]
                except IndexError:
                    return []

                time = ctime().split()[3]

                info['odds']['bet365']      = {"bookie": "Bet365",      "time": time, "price": float(prices[0].attrib['data-odig'])}
                info['odds']['skybet']      = {"bookie": "Skybet",      "time": time, "price": float(prices[1].attrib['data-odig'])}
                info['odds']['ladbrokes']   = {"bookie": "Ladbrokes",   "time": time, "price": float(prices[2].attrib['data-odig'])}
                info['odds']['williamhill'] = {"bookie": "William Hill","time": time, "price": float(prices[3].attrib['data-odig'])}
                info['odds']['betfair']     = {"bookie": "Betfair",     "time": time, "price": float(prices[4].attrib['data-odig'])}
                info['odds']['betvictor']   = {"bookie": "BetVictor",   "time": time, "price": float(prices[5].attrib['data-odig'])}
                info['odds']['paddypower']  = {"bookie": "Paddy Power", "time": time, "price": float(prices[6].attrib['data-odig'])}
                info['odds']['unibet']      = {"bookie": "Unibet",      "time": time, "price": float(prices[7].attrib['data-odig'])}
                info['odds']['coral']       = {"bookie": "Coral",       "time": time, "price": float(prices[8].attrib['data-odig'])}
                info['odds']['betfred']     = {"bookie": "BetFred",     "time": time, "price": float(prices[9].attrib['data-odig'])}
                info['odds']['betway']      = {"bookie": "Betway",      "time": time, "price": float(prices[10].attrib['data-odig'])}
                info['odds']['totesport']   = {"bookie": "Totesport",   "time": time, "price": float(prices[11].attrib['data-odig'])}
                info['odds']['boylesports'] = {"bookie": "Boylesports", "time": time, "price": float(prices[12].attrib['data-odig'])}

                _odds = [info['odds'][bookie] for bookie in info['odds']]
                shuffle(_odds)
                info['best_odds'] = max(_odds, key=lambda k: k['price'])

                race.append(info)

        return race


    def all(self):
        self.races.clear()
        links = self.race_links()

        for link in links:
            self.races[link.split('/')[5]] = self.load_race(link)

        return json.dumps(self.races)

    
    def race(self, race=None):
        self.races.clear()
        
        if race:
            links = self.race_links()

            for link in links:
                if link.split('/')[5] == race:
                    return self.load_race(link)

        return {}


    def list_races(self, meeting=None):
        links = self.race_links()

        if meeting:
            return [link.split('/')[5] for link in links if link.split('/')[4] == meeting]

        return [link.split('/')[5] for link in links]



    def meeting(self, meeting=None):
        self.races.clear()

        if meeting:
            links = self.race_links()

            for link in links:
                if link.split('/')[4] == meeting:
                    self.races[link.split('/')[5]] = self.load_race(link)

            return self.races
            
        return {}


    def list_meetings(self):
        links = self.race_links()
        return list(set([link.split('/')[4] for link in links]))

