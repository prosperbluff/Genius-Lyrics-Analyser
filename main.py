# Packages and libraries
import requests  # Gives us access to HTML and website requests
from bs4 import BeautifulSoup  # Input/Output
import os  # Allow us to search/manipulate strings
import re  # Regular expressions

# Our API token
GENIUS_API_TOKEN = 'u3ct344KisrrhJ53FyYnlM-S1mdceHRJBQBCeCXGeejKQ1oiKJy0JKGOcMU5b4aj'


# Functions
# This just gives us an average from a list.
def average_the_list(lst):
    return sum(lst) / len(lst)


# This searches the api for the artists name and returns data associated with them
def request_artist_info(artist_name, page):
    url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = url + '/search?per_page=20&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# This gives us the list of top x songs related to the artists, and extracts the song titles and lyrics in json form
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


# We then manipulate text to ensure the lyrics are split up, omitting any signifier like [Chorus] etc
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    # remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    # remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
    return lyrics


# Then the final part, putting it all together. The below asks the user to input an artist, and the number of songs
# to analyse. We find the specified number of songs, loop over this list of songs storing the number of lyrics in each
# song into a list, then do a simple average.
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
    print('The average word count for the top ' + str(song_count) + ' ' + artist_name + ' songs is ' + round(str(
        average_the_list(ls))), 2)


if __name__ == "__main__":
    find_lyrics_average()
