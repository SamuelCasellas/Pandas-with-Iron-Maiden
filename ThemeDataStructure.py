from types import NoneType
import re
import concurrent.futures as conc

import pandas as pd
import requests as rq
from bs4 import BeautifulSoup


class ThemeDataStructure:
    """A Data Structure that holds song titles, their accompanying lyrics, the 
    """

    class Themes:

        # Static variables

        OPENING_LINK = "https://www.lexico.com/synonyms/"

        good_vibes = {"righteous", "hope", "joyous", "spiritual", "faith", "fortune", "loyal", "truth", "love", "compassion"}
        bad_vibes = {"evil", "despair", "doom", "terminate", "agony", "slaughter", "death", "rampage", "war", "sad"}
        
        # Initialize the base themes for standard searches
        themes_and_syns = set().union(good_vibes, bad_vibes)

        def __init__(self, custom_theme=None) -> None:
            # Will be modified to a dictionary after retrieving synonyms
            if custom_theme != None:
                self._themes_and_syns = custom_theme
            else:
                self._themes_and_syns = ThemeDataStructure.Themes.themes_and_syns 
        
        def set_syns(self, syns_dic):
            """Converts the above set to a dictionary with the values being lists containing the synonyms
            """
            self._themes_and_syns = syns_dic

        def get_syns(self):
            """If called before the set_synonyms method is called, return a set for all the base themes, else
            return a dictionary with keys as base themes and values as synonyms.
            """
            return self._themes_and_syns
            

    def __init__(self, music_dict, custom_theme=None) -> None:
        self._themes = ThemeDataStructure.Themes(custom_theme)
        self._data_structure = {
            "Songs": music_dict.keys(),
            "Lyrics": music_dict.values() # Not to be displayed
        }

        # Add in themes as well as dictacted by the base_themes set in class Themes
        self._themes.set_syns(self._get_syns_for_themes())
        if type(self._themes.get_syns()) == NoneType:
            print(" No search query for this word. Please try another related word.")
        else:
            self._search_themes()

    def create_pandas_object(self, option):
        df = pd.DataFrame(self._data_structure)
        if option == "good" or option == "bad":
            themes = list(self._themes.get_syns().keys())

            # total the number of occurences for each relating good or bad theme
            for i, theme in enumerate(themes):
                if i == 0:
                    df[option] = df[theme]
                else:
                    df[option] += df[theme]

        for column_name in self._data_structure.keys():
            if column_name != option and column_name != "Songs":
                df.drop(column_name, axis=1, inplace=True)
        try:
            return df.sort_values(option) # Sort with the songs containing most references to the bottom.
        except KeyError:
            return None
        
    def _get_syns_for_themes(self):
        """
        """
        theme_syn_dict = dict()

        def get_synonyms(theme): 
            """Scrape lexicon's synnonyms and return a set containing all of the synonyms listed for one theme
            """
            link = ThemeDataStructure.Themes.OPENING_LINK + theme
            http_req = rq.get(link)
            soup = BeautifulSoup(http_req.text, "html.parser")
            syn_set = soup.findAll(attrs={"class": "syn"})
            syn_string = ""
            for set in syn_set:
                syn_string += set.text
            if len(syn_string) == 0:
                return None
            syns = syn_string.split(",")
            syns = list(map(str.strip, syns))[:10]
            syns.insert(0, theme) # Insert the original word back into the list so the the main theme word can be called.
            return syns

        themes = self._themes.get_syns()
        # Map each theme for faster lookup
        with conc.ThreadPoolExecutor(max_workers=len(themes)) as ex:
            print("Gathering themes and related words...",end="")
            results = ex.map(get_synonyms, themes)
            for result in results:
                try:
                    theme_syn_dict[result[0]] = result

                # No synonyms found since associated page did not exist; bad search.
                except TypeError: 
                    return
            print(" Completed")

        return theme_syn_dict

    def _search_themes(self):
            def populate_theme_occurances(main_theme, syns):
                theme_occurence_for_each_song = []
                for song_lyrics in self._data_structure["Lyrics"]:
                    song_lyrics = re.sub("[,|?|!|.|:|]", "", song_lyrics).lower()
                    song_lyrics = song_lyrics.replace("\n", " ")
                    theme_occurence = 0
                    for word in syns:
                        references = song_lyrics.split(f" {word.lower()} ")
                        theme_occurence += len(references) - 1
                    theme_occurence_for_each_song.append(theme_occurence)
                self._data_structure[main_theme] = theme_occurence_for_each_song
                

            themes_dict = self._themes.get_syns()
            main_themes, syns_of_themes = themes_dict.keys(), themes_dict.values()
            # Map for each theme for faster lookup
            with conc.ThreadPoolExecutor(max_workers=len(themes_dict)) as ex:
                print("\nSearching for themes in songs...", end="")
                ex.map(populate_theme_occurances, main_themes, syns_of_themes)
            print(" Completed")
