from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
import re
import scraperwiki



url = "http://ttparliament.org/members.php?mid=26"
page = urlopen(url)
soup = BeautifulSoup(page)

rows = soup.findAll("tr", { "class" : "trBgOff",  "class": "trBgOn"})
# names = soup.select("td a")


for row in rows:
    id_ = re.search(r";id=(.+)\"", str(row))
    id_ = id_.group(1)

    data = {
       id: id_,
    }

    scraperwiki.sql.save(unique_keys=['id'], data=data)

    
