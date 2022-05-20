# Pandas-with-Iron-Maiden
Here I will dive into the pandas library in Python to analyze the underlying themes in Iron Maiden's music.

# Author: Samuel Casellas
Date of Beta: May 20th, 2022

# Classes
- JsonService:
    - write_dict_to_json(dict): Get a dictionary and write the contents into a json file.
    - read_json_as_dict(): Read a json file into a dictionary
- ThemeDataStructure:
    - Responsibilities: Update, store, and retrieve themes, find occurences of themes in songs, and create a pandas data structure that has columns for names of songs and the requested theme.
    - Behaviors:
        - create_pandas_object(option): create the dataframe that is used which can either:
            a. from all the good/bad themes generate the total count of related themes for each song and return a dataframe object that only contains columns songs and good/bad rating, or
            b. simply return the dataframe object with columns songs and \[theme].
            Param: option - the theme being analyzed.
        - _get_syns_for_themes(): Uses the ThreadPoolExecuter class that generates threads for each theme and looks up related words (synonyms), then returns the results in a dictionary. All themes are mapped into the embedded get_synonyms() function.
        - _search_themes(): Generate threads for each theme to be executed asynchronously and find any sort of matches in each song. The results are included as a key-value pair in the object's data structure (returns nothing). All themes are mapped into the embedded populate_theme_occurances() function.
    - Status:
        - self._themes (Class)
            - Responsibilities: Hold the themes to be used in a standard search with appropriate getters and setters.
            - Behaviors: 
                - get_syns(): get either a set of base themes or a dictionary of the base themes and the synonyms; 
                - set_syns() - input the dictionary that contains the synonyms for the theme.
            - Status: 
                - non-static: 
                    - self._themes_and_syns (String): the set or dictionary of themes. This will vary based on the choice made by the user in the main function.
                - static:
                    - OPENING_LINK (String): a constant holding the beginning of the link for the online thesaurus where the synonyms are retrieved (credit to lexico.com, powered by Oxford).
                    - good_vibes (Set): a set of good themes
                    - bad_vibes (Set): a set of bad themes
                    - themes_and_syns (Set): holds the base themes for standard search; a combination of both good and bad themes
        - self._data_structure (Dictionary): Hold the songs (keyword "Songs"), lyrics for the _search_themes method (keyword "Lyrics"), and the themes and associated with them.

# Overview

Much of software engineering involves analyzing large pieces of data. 
The pandas library in python provides an easy-to-use functions for data analysis. 
I also discovered the robustness of BeautifulSoup for parsing through the document object model (or DOM).

Using these libraries, I analyzed Iron Maidens music and try to find and sort songs for the occurences of various themes, 
either ones that are listed for the user to pick from or custom ones the user provides. 


# Demo
[Software Demo Video](https://youtu.be/x8XrYl_xVKM)

# Data Analysis Results

Technical question: How do I find themes in lyrics?
Brainstorming: Use a library like sentiment or another one I find, or...
Hypothesis: Generate a list of general themes and gather synonyms that relate to that theme.
Iterate through each theme and find occurences of them in the songs.

Questions relating to the dataset:
1. Which songs contain the most evil themes?
    Answer:
    1. Mother of Mercy (25 occurences)
    2. Face in the Sand (21 occurences)
    3. The Evil that Men Do (20 occurences)

2. Which songs contain the most good themes?
    Answer:
    1. Dream of Mirrors (48 occurences)
    2. The Thin Line Between Love & Hate (16 occurences)
    3. The Man Who Would Be Kin (12 occurences)

3. Which songs contain the most references to \[Theme]?
    Answer will depend on the theme...
    For example: If theme is "disappearance":
        Answer:
        1. The Man of Sorrows (4 occurences)
        2. Coming Home (4 occurences)
        3. The Book of Souls (3 occurences)
    
# Development Environment

Programming language: Python

Libraries used:
- Built-in
    - Json (for storing and retrieving the data set)
    - NoneType from types: assessing empty search values
    - re: reformatting the lyrics, such as conveniently removing different punctuation simmultaneously
    - concurrent.futures: creating and mapping threads for fast retrieval of lyrics or synonyms of the themes
- Third-party:
    - Pandas (for arranging of and conducting analysis of data)
    - Requests & BeautifulSoup (scraping lyrics.com for song lyrics and lexicon.com for thesaurus and parsing through the dom for applicable tag names and classes)

# Useful Websites

* [Kaggle.com - The dataset that gave me inspiration](https://www.kaggle.com/code/gabrieldu69/ironmaiden-songs-analysis)
* [Free Code Camp - How to use the drop method for dataframes](https://www.freecodecamp.org/news/drop-list-of-rows-from-pandas-dataframe/)
* [YouTube - Finding a good music site to scrape lyrics from](https://www.youtube.com/watch?v=r8U4s_WAAg8)

# Future Work

* Implement "exact match" for finding direct results of themes/keywords.
* Show a plot of the rating of each theme for the songs as a whole.
* Truncate the search results so that only show the top 5 songs for each search.
* Display the words in the song that related to the theme.
* Implement my catch exception function for making the tree in my main function less dense.
