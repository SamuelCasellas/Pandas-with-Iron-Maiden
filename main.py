import concurrent.futures as conc

import requests as rq
from bs4 import BeautifulSoup

from JsonService import JsonService
from ThemeDataStructure import ThemeDataStructure
    
# Method2, using beautiful soup and getting the song lyrics from a list that contains the URL-ending for all the albums

# Globals

OPENING_URL = "https://www.lyrics.com"

albums_lookups = {
        "Iron Maiden": "/album/9908/Iron-Maiden", # Has an 
        "Killers": "/album/9909/Killers",
        "The Number of the Beast": "/album/584216/The-Number-of-the-Beast-%5BLimited-Edition%5D",
        "Piece of Mind": "/album/9912/Piece-of-Mind",
        "Powerslave": "/album/9913/Powerslave", # Issues, omit "Duellists"
        "Somewhere in Time": "/album/9916/Somewhere-in-Time", # Issues, omit one of track 7 (Deja vu)
        "Seventh Son of a Seventh Son": "/album/9918/Seventh-Son-of-a-Seventh-Son",
        "No Prayer for the Dying": "/album/584450/No-Prayer-for-the-Dying-%5BLimited-Edition%5D",
        "Fear of the Dark": "/album/585219/Fear-of-the-Dark-%5BEnhanced%5D",
        "X Factor": "/album/584761/X-Factor-%5BLimited-Edition%5D",
        "Virtual XI": "/album/346603/Virtual-XI",
        "Brave New World": "/album/484513/Brave-New-World", # Issues, omit wickerman and thin line repeats
        "Dance of Death": "/album/656128/Dance-of-Death", # Issues, omit the remasters for all songs
        "A Matter of Life and Death": "/album/852811/A-Matter-of-Life-and-Death-%5BBonus-DVD%5D",
        "The Final Frontier": "/album/1834298/The-Final-Frontier", # Issues: Omit the 2 other repeats for title track
        "Book of Souls": "/album/3233727/Book-of-Souls-%5BThree-LP%5D",
}

album_adjuster = { # For any repeats found in the albums
    "Powerslave": [4],
    "Somewhere in Time": [7,9],
    "Brave New World": [1,11],
    "Dance of Death": [1,3,5,7,9,11,12,13,14,15,16],
    "The Final Frontier": [1,2]
}

song_lyric_dict = {}


def extract_songs_from_albums(album_number):
    """
    """
    album = list(albums_lookups.keys())[album_number]
    end_link = list(albums_lookups.values())[album_number]

    http_request = rq.get(OPENING_URL+end_link)
    soup = BeautifulSoup(http_request.text, "html.parser")
    songs = soup.findAll("td", {"class": "tal qx fsl"})
    links = []
    if album not in album_adjuster.keys():
        for song in songs[1:][::2]: # omit the track number
            try:
                links.append(OPENING_URL + song.a.attrs["href"])
            except AttributeError: # This is if the song is an instrumental.
                pass
    else:
        for i, song in enumerate(songs[1:][::2]): # omit the track number
            try:
                if i not in album_adjuster[album]:
                    links.append(OPENING_URL + song.a.attrs["href"])
            except AttributeError: # This is if the song is an instrumental.
                pass
    with conc.ThreadPoolExecutor() as ex:
        ex.map(get_lyrics, links)

def get_lyrics(song_page):
    song_http_request = rq.get(song_page)
    soup = BeautifulSoup(song_http_request.text, "html.parser")
    song_name = soup.find("h1", {"id": "lyric-title-text"}).text
    lyrics = soup.find("pre", {"id": "lyric-body-text"}).text
    song_lyric_dict[song_name] = lyrics
    print("Completed lyrics for: ", song_name)
    

def main():

    json_service = JsonService("lyrics.json")
    print("Welcome to finding themes in Iron Maiden music.")
    if input("Do you have a json file with the song lyrics (data set) already downloaded? (y/n) ").lower() == "n":
        with conc.ThreadPoolExecutor() as ex:
            ex.map(extract_songs_from_albums, [i for i in range(0, len(albums_lookups))]) # Map each album for faster lookup
        json_service.write_dict_to_json(song_lyric_dict)
    else:
        while True:
            choose_search_type = input("Would you like to search a custom theme or search from a list? (c, l) ").lower()
            if choose_search_type == "l":
                data = ThemeDataStructure(json_service.read_json_as_dict())
                themes = list(ThemeDataStructure.Themes.themes_and_syns)
                while True:
                    for i, theme in enumerate(themes):
                        print(f"{i+1}. {theme.capitalize()}")
                    num_pick = int(input("Pick a theme you want to analyze: "))
                    theme_pick = themes[num_pick-1]
                    df = data.create_pandas_object(theme_pick)
                    df.drop(df[(df[theme_pick]==0)].index, inplace=True)
                    print(df)
            elif choose_search_type == "c":
                while True:
                    theme_pick = input("Enter theme: ")
                    data = ThemeDataStructure(json_service.read_json_as_dict(), custom_theme=theme_pick)
                    df = data.create_pandas_object(theme_pick)
                    df.drop(df[(df[theme_pick]==0)].index, inplace=True)
                    print(df)
            else:
                print("Try again.")





        # while True:
        #     ask_song = input("Ask song ")
        #     songs = data._data_structure["Songs"]
        #     try:
        #         index = songs.index(ask_song)
        #         print(data._data_structure["Lyrics"][index])
        #     except (ValueError):
        #         pass

if __name__ == "__main__":
    main()