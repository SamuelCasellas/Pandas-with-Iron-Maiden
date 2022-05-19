# Pandas-with-Iron-Maiden
Here I will dive into the pandas library in Python to analyze the underlying themes in Iron Maiden's music.

# My notes

- Two ways to find the themes on the music

- I was able to download the songs faster using threads available from the concurrent.futures library


 -> for figuring out the easiest site to scrape the lyrics from


# Classes
- JsonService:

    - write_dict_to_json(dict): Get a dictionary and write the contents into a json file.
    - read_json_as_dict(): Read a json file into a dictionary
- ThemeDataStructure:
    - Responsibilities: Create a pandas data structure that has columns of name of song and the themes
    - Behaviors:
    - Status:
        - Themes (Class)
            - Responsibilities:
            - Behaviors
            - Status

    

# Overview

Much of software engineering involves large pieces of data that needs analyzing. 
The pandas library in python provides an easy-to-use functions for data analysis. 
I also discovered the robustness of BeautifulSoup for parsing through the document object model (or DOM).


Here I analyze Iron Maidens music and try to find and sort songs for the occurences of various themes, 
either ones that are listed for the user to pick from or custom ones the user provides. 

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the data set, the questions and answers, the code running and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Data Analysis Results

Technical questions:
Question: How do I find themes in lyrics?
Brainstorming: Use a library like sentiment or another one I find, or...
Hypothesis: Generate a list of general themes and gather synonyms that relate to that theme.
Iterate through each theme and 

Questions relating to the dataset:
1. Which songs contain the most evil themes?
2. Which songs contain the most good themes?

Third question:
3. Which songs contain the most references to \[Theme]?

# Development Environment

Programming language: Python

Libraries used:
- Pandas (data analysis)
- Requests and BeautifulSoup (scraping lyrics.com for lyrics to songs and parsing through the dom for applicable tag names and classes)
- concurrent (creating and mapping threads for fast retrieval of lyrics or synonyms of the themes)
- Json (for storing and retrieving the data set)


# Useful Websites

* [Kaggle.com - The dataset that gave me inspiration](https://www.kaggle.com/code/gabrieldu69/ironmaiden-songs-analysis)
* [Free Code Camp - How to use the drop method for dataframes](https://www.freecodecamp.org/news/drop-list-of-rows-from-pandas-dataframe/)
* [YouTube - Finding a good music site to scrape lyrics from](https://www.youtube.com/watch?v=r8U4s_WAAg8)

# Future Work

* Item 1
* Item 2
* Item 3