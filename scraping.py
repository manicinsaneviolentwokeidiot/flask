from bs4 import BeautifulSoup
import requests
import re
import time

def scrape_list(list_url):
    x = 1
    listDictionary = {}
    listDictionary["title"] = []
    listDictionary["movies"] = []
    listDictionary["url"] = list_url
    while True:
        r = requests.get(f"{list_url}/page/{x}")
        soup = BeautifulSoup(r.text, 'lxml')
        films = soup.find_all('ul', class_='js-list-entries poster-list -p125 -grid film-list')
        films2 = films[0].find_all('div', class_='film-poster')
        #print(films2[0])
        for element in films2:
            imgElement = element.find('img')
            url = 'https://letterboxd.com'+element.get('data-target-link')
            listDictionary['movies'].append(scrape_film(url))
        x+=1
        if len(films2) == 0:
            break
    print(listDictionary)
    return listDictionary["movies"]


def scrape_film(url):
    linkname = url.removeprefix('https://letterboxd.com/')
    linkname = 'https://letterboxd.com/csi/'+linkname+'stats/'
    #print(linkname)
    filmdictionary = {}
    r = requests.get(url)
    r2 = requests.get(linkname)
    soup = BeautifulSoup(r.text, 'lxml')
    soup2 = BeautifulSoup(r2.text, 'lxml')
    #print(soup)

    films = soup.find_all('span', class_='name js-widont prettify')
    filmdictionary['title'] = films[0].text
    watches = soup2.find_all('li', class_='stat filmstat-watches')
    print(watches)
    if len(watches) > 0:
        x = watches[0].find('a').get('title')
        x2 = x.lstrip("Watched by ")
        x2 = x2.rstrip(" members")
        x2 = x2.replace(",", "")
        x2 = x2.replace(u'\xa0', u' ')
        x2 = x2.rstrip(" ")
        filmdictionary["watches"] = x2
    print(filmdictionary["watches"])
    return filmdictionary

#y = scrape_film("https://letterboxd.com/film/guardians-of-the-galaxy/")
#print(y)

#scrape_list("https://letterboxd.com/ur_mom_lol/list/letterboxds-1000-most-watched-films/")
scrape_list("https://letterboxd.com/eyesack2007/list/bad-boys-1/")