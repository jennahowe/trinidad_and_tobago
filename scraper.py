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

    rows = soup.findAll("tr", { "class" : ["trBgOff", "trBgOn"]})

    for row in rows:
        url_match = re.search(r'href="(?P<url>.+;id=(?P<id>[^"]+))"', str(row))

        person_url = (base_url + url_match.group('url')).replace('&amp;', '&')
        print "fetching: ", person_url

        id_ = url_match.group('id')
        faction = re.search(r'<td width="140">(?P<faction>.*)</td>', str(row)).group('faction')
        constituency = re.search(r'<td width="200">(?P<constituency>.*)</td>', str(row)).group('constituency')
        name = re.search(r'">(?P<name>.+)</a>', str(row)).group('name')
        name = name.split(', ')
        family_name = name[0]
        given_name = name[1]
        name = "%s %s" % (name[1], name[0])
        # image = scrape_person(person_url)

        data = {
           'id': id_,
           'name': name,
           'given_name': given_name,
           'family_name': family_name,
           'source': person_url,
           'faction': faction,
           'constituency': constituency,
        }
        print data, "\n"
        scraperwiki.sql.save(unique_keys=['id'], data=data)

scrape_list()
