from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
import re
import scraperwiki
import pdb

def scrape_person(person_url):
    page = urlopen(person_url)
    soup = BeautifulSoup(page)



def scrape_list():
    base_url = "http://ttparliament.org"
    list_url = base_url + "/members.php?mid=54"
    page = urlopen(list_url)
    soup = BeautifulSoup(page)

    rows = soup.findAll("tr", { "class" : "trBgOff",  "class": "trBgOn"})

    for row in rows:
        # print row
        # pdb.set_trace()
        url_match = re.search(r'href="([^"]+);', str(row))

        matches = re.search(r';id=(.+)">([^,]+),\s([^<]+)<\/a><\/td><td width="\d+">([^<]+)<\/td><td width="\d+">([^<]+)', str(row))

        id_ = matches.group(1)
        family_name = matches.group(2)
        given_name = matches.group(3)
        name = given_name + " " + family_name
        person_url = base_url + url_match.group(1)

        # image = scrape_person(person_url)

        group = matches.group(4)
        constituency = matches.group(5)

        data = {
           'id': id_,
           'name': name,
           'given_name': given_name,
           'family_name': family_name,
           'source': person_url,
           'group': group,
           'constituency': constituency,
        }
        print data
        # scraperwiki.sql.save(unique_keys=['id'], data=data)


scrape_list()
    
# </tr>
# <tr class="trBgOn"><td class="listRowNum">42.</td>
# <td><a href="/members.php?mid=54&amp;id=SYO14">Young, Stuart</a></td>
# <td width="140">PNM</td>
# <td width="200">Port-of-Spain North/St. Ann's West</td>
# </tr>
