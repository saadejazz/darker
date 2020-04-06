from utils.utils import Indexer, getIP, connectTor, changeIP
from urllib.parse import unquote, quote
from bs4 import BeautifulSoup
from time import time
import requests
import json

class DarkSearch():
    '''Searches and gathers results from the following dark net search engine:
        * not Evil
        * Dark Search 
        * torch 
        * Ahmia
        * Candle
        * tor66     
        * Visitor  
        * Dark Web Links    
        * Onion Land
        * Haystack
        * Deep Link 
        * Grams (For Drugs)
        * MultiVAC   
        * DeepPaste 
    '''
    def __init__(self):
        self.sites = ["not_evil", "dark_search", "torch", "ahmia", "candle", "tor66", "visitor", "dark_web_links", "onion_land",
                      "haystack", "deep_link", "grams", "multivac", "deep_paste"]
        self.session = connectTor()
        self.ip = getIP(self.session)
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"})   
        if self.ip:
            print("Connected to: ", self.ip)

    def __initiateSkeleton(self):
        return {
            "title": "",
            "link": "",
            "description": ""
        }

    @staticmethod
    def cleanQuery(query):
        return "+".join([quote(q) for q in query.split()])

    @staticmethod
    def beautifyText(text):
        return " ".join([a for a in text.replace("\n", "").split() if not a == ""])

    def get(self, url):
        try:
            return self.session.get(url)
        except requests.exceptions.RequestException as err:
            print(f'Error: {err}. Moving on')
            return None

    def not_evil(self, query):
        ''' scrapes not Evil search results '''
        print("Searching not Evil")
        SITE = "https://hss3uro2hsxfogfq.onion.sh/index.php"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        links = []
        for data in soup.find_all('p'):
            d = self.__initiateSkeleton()
            li = data.find('a')
            if li:
                d["title"] = self.beautifyText(li.text)
                d["link"] = unquote(li.get('href', "").partition("?url=")[2].partition("&")[0])
                if d["link"] in links:
                    continue
                else:
                    links.append(d["link"])
            d["description"] = self.beautifyText(data.text)
            results.append(d)
        return results

    def dark_search(self, query):
        ''' GETs results from Dark Search using API. Limit = 30/min '''
        print("Searching Dark Search")
        MAX = 28
        try:
            jso = open("times.json", "r")
        except FileNotFoundError:
            with open("times.json", "w") as jso:
                json.dump([], jso)
            jso = open("times.json", "r")
        read = json.load(jso)
        ti = time()
        read = [j for j in read if ti - j <= 60]
        if len(read) <= MAX:
            read.append(ti)
        else:
            changeIP()
            self.session = connectTor()
            read = []
        with open("times.json", "w") as jso:
            json.dump(read, jso)
        SITE = "https://darksearch.io/api/search"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?query={query}')
        if r.status_code == 200:
            try:
                return json.loads(r.text).get('data', [])
            except:
                print("Check changes to Dark Search API")
        else:
            return []

    def torch(self, query):
        ''' scrapes Torch search results '''
        print("Searching Torch")
        SITE = "http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}&cmd=Search!&ps=20')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for one in soup.find_all('dl'):
            data = self.__initiateSkeleton()
            li = one.find('dt')
            if li:
                li = li.find('a')
                if li:
                    data["title"] = self.beautifyText(li.text)
                    data["link"] = unquote(li.get('href', ""))
                    if data["link"] in links:
                        continue
                    else:
                        links.append(data["link"])
            li = one.find('dd')
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results

    def ahmia(self, query):
        ''' scrapes Ahmia search results '''
        print("Searching Ahmia")
        SITE = "http://msydqstlz2kzerdg.onion/search/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('li', {'class': 'result'}):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["link"] = unquote(li.get('href', "").partition("&redirect_url=")[2].partition("&")[0])
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["title"] = self.beautifyText(li.text)
            li = dat.find('p')
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results

    def candle(self, query):
        ''' scrapes Candle search results '''
        print("Searching Candle")
        SITE = "http://gjobqjj7wyczbqie.onion/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('h2'):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["link"] = unquote(li.get('href', ""))
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["title"] = self.beautifyText(li.text)
            data["description"] = self.beautifyText(BeautifulSoup(str(soup).partition(str(dat.findNext('h3')))[2]
                                      .partition("<h3>")[0].replace("\t", ""), "html.parser").text)
            results.append(data)
        return results
    
    def tor66(self, query):
        ''' scrapes Tor66 search results '''
        print("Searching Tor66")
        SITE = "http://tor66sezptuu2nta.onion/search"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?view=gal&nol=1&q={query}&sorttype=rel&page=1')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text.partition("Onion sites we found")[2], "html.parser")
        for dat in soup.find_all('div', {'class': 'card'}):
            data = self.__initiateSkeleton()
            li = dat.find('div', {'class': 'header'})
            if li:
                li = li.find('a')
                if li:
                    data["link"] = unquote(li.get('href', ""))
                    if data["link"] in links:
                        continue
                    else:
                        links.append(data["link"])
                    data["title"] = self.beautifyText(li.text)
            li = dat.find('div', {'class': 'meta'})
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results
    
    def visitor(self, query):
        ''' scrapes Visitor search results '''
        print("Searching Visitor")
        SITE = "http://visitorfi5kl7q7i.onion/search/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('li', {'class': 'hs_site'}):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["link"] = unquote(li.get('href', ""))
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["title"] = self.beautifyText(li.text)
            li = dat.find('div', {'class': 'infotext'})
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results

    def dark_web_links(self, query):
        ''' scrapes Dark Web Links search results '''
        print("Searching Dark Web Links")
        SITE = "http://www.bznjtqphs2lp4xdd.onion/cgi-bin/search/search.pl"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?Realm=My%20Realm%201&Match=0&Terms={query}&sort-method=1&maxhits=20&Rank=1')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('dd', {'class': 'sr'}):
            data = self.__initiateSkeleton()
            li = dat.text
            data["link"] = unquote(self.beautifyText(li.partition("URL: -> ")[2].partition(" ")[0]))
            if data["link"] in links:
                continue
            else:
                links.append(data["link"])
            data["title"] = self.beautifyText(li.partition("Title: - ")[2].partition("\n")[0])
            data["description"] = self.beautifyText(li.partition("Description: - ")[2].partition("Legal Notice - ")[0])
            results.append(data)
        return results
    
    def onion_land(self, query):
        ''' scrapes Onion Land search results '''
        print("Searching Onion Land")
        SITE = "http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('div', {'class': 'result-block'}):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                if li.get("data-category") == "sponsored-text":
                    continue
                data["title"] = self.beautifyText(li.text)
            li = dat.find('div', {'class': 'link'})
            if li:
                data["link"] = self.beautifyText(li.text)
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
            li = dat.find('div', {'class': 'desc'})
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results

    def haystack(self, query):
        ''' scrapes Haystack search results '''
        print("Searching Haystack")
        SITE = "http://haystakvxad7wbk5.onion/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('div', {'class': 'result'}):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["title"] = self.beautifyText(li.text)
            li = dat.find('i')
            if li:
                data["link"] = unquote(self.beautifyText(li.text))
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["description"] = self.beautifyText(BeautifulSoup(str(soup).partition(str(li))[2].partition("<a")[0], "html.parser").text)
            results.append(data)
        return results

    def deep_link(self, query):
        ''' Deep Link search results '''
        print("Searching Deep Link")
        SITE = "http://deeplinkdeatbml7.onion/"
        query = self.cleanQuery(query)
        self.get(f'{SITE}?search={query}&type=verified')
        r = self.get(f'{SITE}?search={query}&type=verified')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        tr = soup.find_all('tr')
        if tr != []:
            tr = tr[1:]
        for dat in tr:
            data = self.__initiateSkeleton()
            li = dat.find_all('td')
            if len(li) >= 3:
                a = li[0].find('a')
                if a:
                    data["link"] = unquote(a.get('href', ''))
                    if data["link"] in links:
                        continue
                    else:
                        links.append(data["link"])
                data["title"] = self.beautifyText(li[1].text)
                data["description"] = self.beautifyText(li[2].text)
            results.append(data)
        return results

    def grams(self, query):
        ''' scrapes Grams search results '''
        print("Searching Grams")
        SITE = "http://grams7ebnju7gwjl.onion/results/index.php"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?searchstr={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('div', {'class': 'media-body'}):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["link"] = unquote(li.get('href', ""))
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["title"] = self.beautifyText(li.text)
            data["description"] = self.beautifyText(dat.text.replace(data["link"], "").replace(data["title"], ""))
            results.append(data)
        return results

    def multivac(self, query):
        ''' scrapes MultiVAC search results '''
        print("Searching MultiVAC")
        SITE = "http://multivacigqzqqon.onion/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}?q={query}&submit=Submit')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text, "html.parser")
        for dat in soup.find_all('dl'):
            data = self.__initiateSkeleton()
            li = dat.find('a')
            if li:
                data["link"] = unquote(li.get('href', ""))
                if data["link"] in links:
                    continue
                else:
                    links.append(data["link"])
                data["title"] = self.beautifyText(li.text)
            li = dat.find('dd')
            if li:
                data["description"] = self.beautifyText(li.text)
            results.append(data)
        return results

    def deep_paste(self, query):
        ''' scrapes Deep Paste search results '''
        print("Searching Deep Paste")
        SITE = "http://4m6omb3gmrmnwzxi.onion/"
        query = self.cleanQuery(query)
        r = self.get(f'{SITE}show.php?keyword={query}')
        if not r:
            return []
        results = []
        links = []
        soup = BeautifulSoup(r.text.partition("Title Matches")[2].partition("<span ")[0].partition("<input ")[0], "html.parser")
        for dat in soup.find_all('a'):
            data = self.__initiateSkeleton()
            data["link"] = SITE + unquote(dat.get('href', "").replace("\n", ""))
            if data["link"] in links:
                continue
            else:
                links.append(data["link"])
            data["title"] = self.beautifyText(dat.text)
            results.append(data)
        return results

    def searchDarkWeb(self, query, include = None, exclude = None):
        ''' Gets data from search engines specified '''
        if include:
            final = [a for a in include if a in self.sites]
        elif exclude:
            final = [a for a in self.sites if a not in exclude]
        else:
            final = self.sites
        
        results = []
        if "torch" in final:
            results += self.torch(query)
        if "not_evil" in final:
            results += self.not_evil(query)
        if "dark_search" in final:
            results += self.dark_search(query)
        if "candle" in final:
            results += self.candle(query)
        if "tor66" in final:
            results += self.tor66(query)
        if "visitor" in final:
            results += self.visitor(query)
        if "dark_web_links" in final:
            results += self.dark_web_links(query)
        if "onion_land" in final:
            results += self.onion_land(query)
        if "haystack" in final:
            results += self.haystack(query)
        if "ahmia" in final:
            results += self.ahmia(query)
        if "deep_link" in final:
            results += self.deep_link(query)
        if "grams" in final:
            results += self.grams(query)
        if "multivac" in final:
            results += self.multivac(query)
        if "deep_paste" in final:
            results += self.deep_paste(query)

        ind = Indexer()
        for i in results:
            ind.join(i)
        
        return ind.results()

