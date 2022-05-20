import concurrent.futures as conc

import requests as rq
from bs4 import BeautifulSoup

from JsonService import JsonService
from ThemeDataStructure import ThemeDataStructure

# Globals

OPENING_URL = "https://www.lyrics.com"

albums_lookups = {
        "Iron Maiden": "/album/9908/Iron-Maiden",
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
    """Manage each album and make appropriate adjustments for extracting each song link provided in the table 
    (format can vary from page to page). Thread each album with the concurrent.futures module for faster lookup.
    """
    # These albums on the website include the cd number and must be accounted for
    cd_albums = {"Virtual XI", "Brave New World", "Dance of Death", "Book of Souls"}

    album = list(albums_lookups.keys())[album_number]
    end_link = list(albums_lookups.values())[album_number]

    http_request = rq.get(OPENING_URL+end_link)
    soup = BeautifulSoup(http_request.text, "html.parser")
    songs = soup.findAll("td", {"class": "tal qx fsl"})
    
    # These albums include a column for cd #, which of course we don't want.
    if album in cd_albums:
        starting_number = 2 
        # Jump count incremented yet again since for all associated pages 
        # the elements for the track length now have the same class name.
        jump_count = 4 
        # Strangely, this is the only album that includes a column including artist name.
        # Jump over this column as well.
        if album == "Virtual XI":
            jump_count += 1
    else:
        starting_number = 1
        jump_count = 2

    song_links = []
    # For albums with no repeated songs
    if album not in album_adjuster.keys():
        # omit the track number
        for song in songs[starting_number:][::jump_count]: 
            try:
                song_links.append(OPENING_URL + song.a.attrs["href"])
            # Song is an instrumental
            except AttributeError: 
                pass
    # For albums with repeated songs
    else:
        # omit the track number
        for i, song in enumerate(songs[starting_number:][::jump_count]): 
            try:
                if i not in album_adjuster[album]:
                    song_links.append(OPENING_URL + song.a.attrs["href"])
            # Song is an instrumental
            except AttributeError:
                pass
    # Map each of the album's songs for faster lookup.
    with conc.ThreadPoolExecutor() as ex:
        ex.map(get_lyrics, song_links)

def get_lyrics(song_page):
    song_http_request = rq.get(song_page)
    soup = BeautifulSoup(song_http_request.text, "html.parser")
    song_name = soup.find("h1", {"id": "lyric-title-text"}).text
    lyrics = soup.find("pre", {"id": "lyric-body-text"}).text
    song_lyric_dict[song_name] = lyrics
    print("Completed lyrics for: ", song_name)
    

def main():
    json_service = JsonService("lyrics.json")

    print("\n"*50)
    while True:
        print("Welcome to finding themes in Iron Maiden music.")
        verify_json = input("Do you have a json file with the song lyrics (data set) already downloaded? (y/n) ").lower()
        match verify_json:
            case "n":
                # Map each album for faster lookup
                with conc.ThreadPoolExecutor() as ex:
                    ex.map(extract_songs_from_albums, [i for i in range(0, len(albums_lookups))])
                json_service.write_dict_to_json(song_lyric_dict)
                print("Lyric retrieval completed.")
            case "y":
                # Main loop: 
                # repeat theme searches
                while True:
                    choose_search_type = input("Would you like to search a Custom theme or search from a List of options?\n\
You can also measure Good and Bad elements for each song\n(select from c, l, g, b) -> ").lower()
                    match choose_search_type:
                        case "l":
                            data = ThemeDataStructure(json_service.read_json_as_dict())
                            themes = list(ThemeDataStructure.Themes.themes_and_syns)
                            while True:
                                for i, theme in enumerate(themes):
                                    print(f"{i+1}. {theme.capitalize()}")
                                num_pick = int(input("\nPick a theme you want to analyze: "))
                                try:
                                    theme_pick = themes[num_pick-1]
                                except IndexError:
                                    print("\nNumber mismatch.\n")
                                    break
                                
                                # Create a data frame according to the theme chosen
                                df = data.create_pandas_object(theme_pick)

                                # Drop any songs that had no matches
                                df.drop(df[(df[theme_pick]==0)].index, inplace=True) 
                                print(df, "\n")

                        case "c":
                            while True:
                                theme_pick = input("\nEnter theme: ")
                                data = ThemeDataStructure(json_service.read_json_as_dict(), custom_theme={theme_pick})
                                df = data.create_pandas_object(theme_pick)
                                
                                try:
                                    # Drop any songs that had no matches
                                    df.drop(df[(df[theme_pick]==0)].index, inplace=True)
                                    if len(df) != 0:
                                        print(df)
                                    else:
                                        print("\nNo references found.")
                                # if NoneType due to a bad search.
                                except AttributeError: 
                                    pass

                        case "g":
                            data = ThemeDataStructure(json_service.read_json_as_dict(), custom_theme=ThemeDataStructure.Themes.good_vibes)
                            df = data.create_pandas_object("good")

                            # Drop any songs that had no matches
                            df.drop(df[(df["good"]==0)].index, inplace=True)
                            print(df, "\n")
                            print("Total good theme references: {}".format(df["good"].sum()))
                        case "b":
                            data = ThemeDataStructure(json_service.read_json_as_dict(), custom_theme=ThemeDataStructure.Themes.bad_vibes)
                            df = data.create_pandas_object("bad")

                            # Drop any songs that had no matches
                            df.drop(df[(df["bad"]==0)].index, inplace=True)
                            print(df, "\n")
                            print("Total bad theme references: {}".format(df["bad"].sum()))
                        case _:
                            print("\nTry again.\n")
            case _:
                print("\nTry again.\n")
                
if __name__ == "__main__":
    main()