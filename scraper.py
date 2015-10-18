from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import scraperwiki
import pdb
import time

sleep_between_requests = 5 # (seconds)
base_url = "http://ttparliament.org"
current_reps_url = base_url + "/members.php?mid=54"
current_senate_url = base_url + "/members.php?mid=55"
term = "11th Republican Parliament" # Can't be scraped from anywhere

def scrape_person(person_url):
    page = urlopen(person_url)
    soup = BeautifulSoup(page)

    image = soup.findAll("img", {"class": "img"})[0]
    image = re.search(r'src="(?P<url>.+)"\s', str(image)).group('url')

    return image

def split_name(name):
    name = name.split(', ')

    family_name = name[0]
    given_name = name[1]
    name = "%s %s" % (name[1], name[0])

    return (name, given_name, family_name)

def create_entry(id_='', name='', source='', faction='', image='', 
              constituency=False, term=''):
    name, given_name, family_name = split_name(name)

    data = {
               'id': id_,
               'name': name,
               'given_name': given_name,
               'family_name': family_name,
               'source': source,
               'faction': faction,
               'image': image,
               'term': term
            }
    if constituency:
        data['constituency'] = constituency

    return data

# def scrape_past():

    
def scrape_current(url, house):
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
        image = base_url + scrape_person(person_url)

        if house == "reps":
            table_name = 'house_of_representatives'
            data = create_entry(id_=id_, name=name, source=person_url,
                                faction=faction, image=image,
                                constituency=constituency, term=term, 
                                )


        elif house == "senate":
            table_name = 'senate'
            data = create_entry(id_=id_, name=name, source=person_url,
                                faction=faction, image=image, term=term, 
                                )


        print data, "\n"
        scraperwiki.sql.save(unique_keys=['id'], data=data, 
                             table_name=table_name)

        time.sleep(sleep_between_requests)

# scrape_current(current_reps_url, "reps")
scrape_current(current_senate_url, "senate")
