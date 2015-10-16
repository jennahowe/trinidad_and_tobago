from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
import re
import scraperwiki
import pdb

# def scrape_person(person_url):
#     page = urlopen(person_url)
#     soup = BeautifulSoup(page)


def scrape_list():
    base_url = "http://ttparliament.org"
    list_url = base_url + "/members.php?mid=54"
    page = urlopen(list_url)
    soup = BeautifulSoup(page)

    rows = soup.findAll("tr", { "class" : ["trBgOff", "trBgOn"]})

    for row in rows:
        url_match = re.search(r'href="(?P<url>.+;id=(?P<id>[^"]+))"', str(row))

        # id_ = matches.group(1)
        # family_name = matches.group(2)
        # given_name = matches.group(3)
        # name = given_name + " " + family_name
        person_url = (base_url + url_match.group('url')).replace('&amp;', '&')
        print "fetching: ", person_url

        id_ = url_match.group('id')
        faction = re.search(r'<td width="140">(?P<faction>.*)</td>', str(row)).group('faction')
        constituency = re.search(r'<td width="200">(?P<constituency>.*)</td>', str(row)).group('constituency')

        # image = scrape_person(person_url)

        # faction = matches.group(4)
        # constituency = matches.group(5)

        data = {
           'id': id_,
           # 'name': name,
           # 'given_name': given_name,
           # 'family_name': family_name,
           'source': person_url,
           'faction': faction,
           'constituency': constituency,
        }
        print data, "\n"
        scraperwiki.sql.save(unique_keys=['id'], data=data)

scrape_list()
    
# </tr>
# <tr class="trBgOn"><td class="listRowNum">42.</td>
# <td><a href="/members.php?mid=54&amp;id=SYO14">Young, Stuart</a></td>
# <td width="140">PNM</td>
# <td width="200">Port-of-Spain North/St. Ann's West</td>
# </tr>
