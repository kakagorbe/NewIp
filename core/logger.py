import time
import json

class Metrics:
    def __init__(self):
        self.counters = {}

    def inc(self, key):
        self.counters[key] = self.counters.get(key, 0) + 1

    def get(self, key):
        return self.counters.get(key, 0)

def get_logger(name):
    class Logger:
        def info(self, data):
            print(json.dumps({"logger": name, "time": time.time(), **data}))
    return Logger()
