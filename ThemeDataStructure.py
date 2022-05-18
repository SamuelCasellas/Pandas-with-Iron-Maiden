import pandas as pd
import requests as rq
import concurrent.futures as conc
from bs4 import BeautifulSoup

class ThemeDataStructure:
    """A Data Structure that holds song titles, their accompanying lyrics, the 
    """

    class Themes:

        OPENING_LINK = "https://www.lexico.com/synonyms/"
        
        def __init__(self) -> None:
            self._themes_and_syns = {
                "despair",
                "despise",
                "hope",
                "peace",
                "awe-inspiring",
                "frenzied",
                "doomed",
                "terminate",
                "shameful",
                "sad",
                "mystical",
                "love",
                "agony",
                "grief",
                "wicked"
            }
        
        def set_synonyms(self, syns_dic):
            """Converts the above set to a dictionary with the values being lists containing the synonyms
            """
            self._themes_and_syns = syns_dic

        def get_syns(self):
            """Not to be called until set_synonyms has been used once
            """
            return self._themes_and_syns
            

    def __init__(self, music_dict) -> None:
        self._themes = ThemeDataStructure.Themes()
        self._data_structure = {
            "Songs": [song for song in music_dict.keys()],
            "Lyrics": [lyrics for lyrics in music_dict.values()] # Not to be displayed
        }

        # #####
        # old_set = self._themes.get_syns()

        # Add in themes as well as dictacted by the base_themes set in class Themes
        self._themes.set_synonyms(self._get_syns_for_themes(self._themes))
        self._search_themes()

        # i = 0
        # for theme in old_set:
        #     try:
        #         print(f"HELLO {i}", self._themes.get_syns()[theme])
        #         i += 1
        #     except KeyError as err:
        #         raise KeyError(f"{err}: Processing of themes has not completed!")

    # def display_songs(self): # debugging
    #     self._data_structure["Songs"].sort()
    #     print(self._data_structure["Songs"])
               

    def create_pandas_object(self):
        df = pd.DataFrame(self._data_structure)
   #     df.drop(, inplace=True)
        print(df)

    def display_data_structure(option):
        pass

    def _get_syns_for_themes(self, themes_object): # DONE BETA
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
            syns = syn_string.split(",")
            syns = list(map(str.strip, syns))
            syns.insert(0, theme) # Insert the original word back into the list so the the main theme word can be called.
            return syns

        themes = [theme for theme in themes_object._themes_and_syns]
        with conc.ThreadPoolExecutor(max_workers=len(themes)) as ex:
            print("Gathering themes and related words...",end="")
            results = ex.map(get_synonyms, themes)
            for result in results:
                theme_syn_dict[result[0]] = result
            print(" Completed")
        
        return theme_syn_dict

    def _search_themes(self):
            def populate_theme_occurances(main_theme, syns):
                theme_occurence_for_each_song = []
                for song_lyrics in self._data_structure["Lyrics"]:
                    theme_occurence = 0
                    for word in syns:
                        if song_lyrics.__contains__(word):
                            theme_occurence += 1
                    theme_occurence_for_each_song.append(theme_occurence)
                self._data_structure[main_theme] = theme_occurence_for_each_song
                

            themes_dict = self._themes.get_syns()
            main_themes, syns_of_themes = themes_dict.keys(), themes_dict.values()

            with conc.ThreadPoolExecutor(max_workers=len(themes_dict)) as ex:
                print("\nSearching for themes in songs...", end="")
                ex.map(populate_theme_occurances, main_themes, syns_of_themes)
            print(" Completed")