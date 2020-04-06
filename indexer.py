

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
