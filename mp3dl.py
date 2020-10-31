from bs4 import BeautifulSoup
from collections import deque
import requests
import wget
import ssl

headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

#  _.mp3?_=2
ssl._create_default_https_context = ssl._create_unverified_context

def clean(song_link):
    if song_link is None:
        return None
    song = song_link[-4:]
    if song != ".mp3":
        song_link = song_link[:-4]
    return song_link

def getSongLinks(url):
    print("processing url: %s" %url)
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    x = soup.find_all("audio")
    print("audio tags found: %d" %len(x))
    fruits=set()
    for a in x:
        song_link = a.get('src')
        print(song_link)
        song_link = clean(song_link)
        if song_link is not None and song_link not in fruits:
            fruits.add(song_link)
            fileName = wget.download(song_link, out="./songs/")
            print("Downloaded : %s" %fileName)

    x = soup.find_all("source", type="audio/mpeg")    
    print("source tags found: %d" %len(x))
    for a in x:
        song_link = a.get('src')
        song_link = clean(song_link)
        print(song_link)
        if song_link is not None and song_link not in fruits:
            fruits.add(song_link)
            fileName = wget.download(song_link, out="./songs/")
            print("Downloaded : %s" %fileName)
    return fruits    


base = "http://www.oldisgold.co.in"
fresh = deque([base])
processed = set()
local = set()
foreign = set()
broken = set()
fruits=set()
while len(fresh):
    url = fresh.popleft()
    processed.add(url)
    fruits.update(getSongLinks(url))
    print("songs fetched: %d" %len(fruits))
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    for link in soup.find_all('a'):
        anchor = link.attrs["href"] if  "href" in link.attrs else ""
        # print("recurse on: %s" %anchor)
        if "www.oldisgold.co.in" in anchor and anchor not in processed:
            local.add(anchor)
            fresh.append(anchor)

print("finished fetching links")
    



