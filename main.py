


GENIUS_API_TOKEN='u3ct344KisrrhJ53FyYnlM-S1mdceHRJBQBCeCXGeejKQ1oiKJy0JKGOcMU5b4aj'


# Make HTTP requests
import requests # Scrape data from an HTML document
from bs4 import BeautifulSoup # I/O
import os # Search and manipulate strings
import re
import statistics

def average_the_list(lst):
    return sum(lst) / len(lst)

def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=20&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


def request_song_url(artist_name, song_cap):
    page = 1
    songs = []

    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()  # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)

        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)

        if (len(songs) == song_cap):
            break
        else:
            page += 1

    print('Found the top {} songs by {}'.format(len(songs), artist_name))
    return songs

def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics

def find_lyrics_average():
    artist_name = input("Please choose an artist: ")
    song_count = input("Please choose the number of songs to analyse: ")
    urls = request_song_url(artist_name, int(song_count))
    ls = []
    for url in urls:
        lyrics = scrape_song_lyrics(url)
        count = len(lyrics.split())
        ls.append(count)
    most = max(ls)
    print('The average word count for the top ' + str(song_count) + ' ' + artist_name + ' songs is ' + str(average_the_list(ls)))
    return average_the_list(ls)

