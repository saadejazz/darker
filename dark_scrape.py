from .utils import getIP, connectTor
from html2text import HTML2Text
from bs4 import BeautifulSoup
import validators
import lxml.etree
import lxml.html
import requests
import re

class DarkScrape():
    '''Scrapes data from an onion site. Data scraped consists of:
        * emails
        * links
        * images
        * text
        * title
        * bitcoin addresses
        if available.
    '''
    def __init__(self):
        self.session = connectTor()
        self.ip = getIP(self.session)
        if self.ip:
            print("Connected to: ", self.ip)
        self.response = ""
        self.markdown = ""
        self.url = ""
        self.soup = BeautifulSoup("", "html.parser")

    def emails(self):
        k = re.findall(r'[\w\.-]+@[\w\.-]+', str(self.response))
        return list(set([a for a in k if validators.email(a)]))
        
    def links(self):
        links = [g.get('href') for g in self.soup.find_all('a')]
        links = [str(l) for l in links if validators.url(str(l))]
        links += [a.replace(a.partition(".onion")[2], "") for a in re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.response)]
        return list(set(links))
    
    def images(self):
        links = [g.get('src') for g in self.soup.find_all(lambda tag: tag.name in ["i", "img", "a"]) if g.get('src')]
        return list(set([str(l) for l in links if validators.url(str(l))]))
    
    def text(self):
        root = lxml.html.fromstring(self.response)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")
        text = lxml.html.tostring(root, method = "text", encoding = "unicode").replace("\r \r", "\n").replace("\n", " ").replace("\r", "")
        self.markdown = HTML2Text().handle(text)
        return text

    def title(self):
        return self.soup.title.text

    def bitcoins(self):
        return list(set(re.findall(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', self.response)))
    
    def scrape(self, url):
        if not validators.url(url):
            print("Invalid URL")
            return self
        try:
            try:
                r = self.session.get(url, timeout = 10)
            except requests.exceptions.Timeout:
                print("Request Timed out.")
                return self
            if r.status_code == 200:
                self.response = r.text
            else:
                print("Response: ", r.status_code)
        except requests.exceptions.RequestException as err:
            print("Error: ", err)
            return self
        self.url = url
        self.soup = BeautifulSoup(self.response, "html.parser")
        return self
    
    @property
    def result(self): 
        return {
            "url": self.url,
            "title": self.title(),
            "links": self.links(),
            "emails": self.emails(),
            "images": self.images(),
            "text": self.text(),
            "bitcoin": self.bitcoins()
        }
    