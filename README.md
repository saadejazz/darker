# Dark Web Search and Scrape  

## Getting started  
In the working directory of your top level python script:  
```bash
mkdir darker
cd darker
git init
git add .
git remote add https://github.com/saadejazz/darker
git pull darker master
```
Install the following python packages using pip  
* [requests](https://github.com/psf/requests)  
* [bs4](https://github.com/getanewsletter/BeautifulSoup4)  
* [stem](https://github.com/torproject/stem)  
* [lxml](https://github.com/lxml/lxml/) 
* [html2text](https://github.com/aaronsw/html2text)  
* [validators](https://github.com/kvesteri/validators) 
* [regex](https://bitbucket.org/mrabarnett/mrab-regex)  

```bash
python -m pip install requests bs4 stem lxml html2text validators regex
```

## Dark Web Meta Searcher  
Scrapes search results from the following dark web search engines:  
* [not Evil](https://hss3uro2hsxfogfq.onion.sh/index.php)  
* [Dark Search](https://darksearch.io)  
* [Torch](http://xmh57jrzrnw6insl.onion/4a1f6b371c/search.cgi)  
* [Ahmia](http://msydqstlz2kzerdg.onion/search/)  
* [Candle](http://gjobqjj7wyczbqie.onion/)  
* [Tor66](http://tor66sezptuu2nta.onion/search)  
* [Visitor](http://visitorfi5kl7q7i.onion/search/)  
* [Dark Web Links](http://www.bznjtqphs2lp4xdd.onion/cgi-bin/search/search.pl)  
* [Onion Land](http://3bbad7fauom4d6sgppalyqddsqbf5u5p56b5k5uk2zxsy3d6ey2jobad.onion/search)  
* [Haystack](http://haystakvxad7wbk5.onion/)  
* [Deep Link](http://deeplinkdeatbml7.onion/)  
* [Grams](http://grams7ebnju7gwjl.onion/results/index.php)  
* [multiVAC](http://multivacigqzqqon.onion/)  
* [Deep Paste](http://4m6omb3gmrmnwzxi.onion/)

**Code:**  
```python
from darker.dark_search import DarkSearch

query = "guns"
results = DarkSearch().searchDarkWeb(query)
print(results)

```
**Example Output:**  
```python
{
  'title': 'Euro Guns - Number one guns dealer in onionland - Buy guns and ammo for Bitcoin.',
  'link': 'http://2kka4f23pcxgqkpv.onion/',
  'description': 'Buy guns for Bitcoin with Euroguns, best deep web arms dealer. Buy guns without a permit.',
  'score': 3
  }
```
The search results are sorted according to frequency of occurence (score).  

## Dark Web generic scrapper  
Scrapes a target web-page on the dark-web 
The scraper provides the following attributes as a result:  
* Title  
* Links  
* Emails  
* Images  
* Text  
* Bitcoin addresses  

**Code:**  
```python
from darker.dark_scrape import DarkScrape

target = "http://4m6omb3gmrmnwzxi.onion/show.php?md5=f6c5d3bc1683338f103b18951b725551"
d = DarkScrape().scrape(target)
print(d.result) # for above-mentioned attributes
print(d.markdown) # for text in markdown format (thanks to html2text)

```

**Output:**  
```python
{
 'title': 'DeepPaste',
 'links': [],
 'emails': ['shootteam@protonmail.com'],
 'images': [],
 'text': '\r \r Hello Anon - Login\r DeepPaste\r Your Deep-Shit Hoster for special shit\r \r Results for f6c5d3bc1683338f103b18951b725551:hand guns and riffles Anon, March 27, 2019 - 4:32 am UTCbuy guns, full auto assault rifles, pistols, grenade launchers, etc.we ship all around america and europe.for more info or questions contact us via shootteam@protonmail.comViews: 1937 \xa0\xa0 Voting: 0 \xa0 ↑ Up \xa0 ↓ DownLogin to voteComments:-__________________________________Add a comment:Name: Anon  Captcha:    \r \r \r Last Public Pastes\r Top Last Public Pastes\r Search Pastes... \r Infos about DeepPaste\r \r For new tea:BTC: 14US287mkpaMYFszkSw2dcEZtdMi3UQak6\r Views Today: 110.432 - Views Yesterday: 337.759\r \r \r \r ',
 'bitcoin': []
 }
```
