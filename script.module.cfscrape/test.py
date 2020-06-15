from datetime import datetime
from lib import cfscrape

scraper = cfscrape.create_scraper()

print datetime.now()

def test(i):
    result = scraper.get(i)
    print result.status_code

lists = ["https://hdfilme.cc/", "https://hd-streams.org/", "https://kinox.to"]

for i in lists:
    result = scraper.get(i)
    print result.status_code
print datetime.now()

from threading import Thread
threads = []
for i in lists:
    threads.append(Thread(target=test, args=(i,)))

for i in threads:
    i.start()

[i.join() for i in threads]

print datetime.now()