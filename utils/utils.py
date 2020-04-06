# pylint: disable=no-member
from stem import Signal
from stem.control import Controller
import requests


def getIP(session):
    try:
        r = session.get('http://httpbin.org/ip')
    except requests.exceptions.RequestException as err:
        print(err, " Could not locate IP")
        return None
    jso = None
    if r.status_code == 200:
        try:
            jso = json.loads(r.text).get('origin', None)
        except:
            pass
    return jso

def connectTor():
    try:
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'
    except Exception as exc:
        print("Check if tor is running")
        raise exc
    return session

def changeIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


class Indexer():
    def __init__(self):
        self.dictionary = {}

    def join(self, arg):
        key = arg.get("link")
        if key is not None:
            if self.dictionary.get(key) is None:
                self.dictionary[key] = dict(arg)
                self.dictionary[key].update({'score': 1})
            else:
                self.dictionary[key]["score"] += 1
        else:
            print("Wrong argument")
        return self

    def results(self):
        final = sorted(list(self.dictionary.values()), key = lambda x: x["score"], reverse = True)
        return final
