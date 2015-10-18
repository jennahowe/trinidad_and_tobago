from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
import re
import scraperwiki
import pdb
import time

sleep_between_requests = 5 # (seconds)
base_url = "http://ttparliament.org"
reps_url = base_url + "/members.php?mid=54"
senate_url = base_url + "/members.php?mid=55"
term = "11th Republican Parliament" # Can't be scraped from anywhere

def scrape_person(person_url):
    page = urlopen(person_url)
    soup = BeautifulSoup(page)

    image = soup.findAll("img", {"class": "img"})[0]
    image = re.search(r'src="(?P<url>.+)"\s', str(image)).group('url')

    return image
    
def scrape_list(url, house):
    page = urlopen(url)
    soup = BeautifulSoup(page)

    rows = soup.findAll("tr", { "class" : ["trBgOff", "trBgOn"] })

    for row in rows:
        url_match = re.search(r'href="(?P<url>.+;id=(?P<id>[^"]+))"', str(row))

        person_url = (base_url + url_match.group('url')).replace('&amp;', '&')
        print "fetching: ", person_url

        id_ = url_match.group('id')
        faction = (re.search(r'<td width="140">(?P<faction>.*)</td>', str(row))
                    .group('faction'))

        if house == "reps":
            constituency = re.search(r'<td width="200">(?P<constituency>.*)</td>',
                                     str(row)).group('constituency')

        name = re.search(r'">(?P<name>.+)</a>', str(row)).group('name')
        name = name.split(', ')

        family_name = name[0]
        given_name = name[1]
        name = "%s %s" % (name[1], name[0])
        image = base_url + scrape_person(person_url)

        data = {
               'id': id_,
               'name': name,
               'given_name': given_name,
               'family_name': family_name,
               'source': person_url,
               'faction': faction,
               'image': image,
               'term': term
            }

        if house == "reps":
            data['constituency'] = constituency
            table_name = 'house_of_representatives'

        elif house == "senate":
            table_name = 'senate'


        print data, "\n"
        scraperwiki.sql.save(unique_keys=['id'], data=data, 
                             table_name=table_name)

        time.sleep(sleep_between_requests)

scrape_list(reps_url, "reps")
scrape_list(senate_url, "senate")
