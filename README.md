# Easy_chatbot Game recomendation
Bender ChatBot recommend videogames
________________________________________________________________________________________________________________________________________________________________________
I am currently creating this chatbot as part of a professional training. There are small bugs that need to be polished.
________________________________________________________________________________________________________________________________________________________________________

The Berder ChatBot recommends 10 games in a gui, the recommendations are taken from the Metacritic page using webScraping, the critic are taken only from the accredited media. To get the data you have to run the Meta_scraping file, which will storage the datas in a MongoDB.

This project consists of 4 parts:
- Web Scraping
- Recommendation System
- Chatbot logic
- Graphical Enviroment


### Web scraping Metacritic -> meta_scraping.py
  
* The scraping phase consists of 2 phases: 
- The first one takes the main page of the best games of all times and returns a list with the names of the games, the platform, the release date and the metascore and the url, and storage the dict in a json archive.

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/Meta%20all%20games.png" width="50%" height="50%">

- In the second one, take out the url per games in dict_games to scraped the critic reviews, date, note and url of the reviewers and update the games.json *

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/games.png" width="50%" height="50%">


### Implement recommendation system: recomend_sys.py

*   the recommendation system takes the rating that each media has given to each game and creates a covariance matrix with the list of favorite games that the user has entered. Return a list with the most recommended games in first place:

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/recomen_sys.png" width="50%" height="50%">

### ChatBoot . ->chatbot_meta.py

* Attached summary flowchart of the chatbot

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/Chat_bot-Diagram.png" width="50%" height="50%">

### Graphical Environment With TK. -> main.py

* The chatbot is implemented with the Tkinter library.

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/chatbot_1.png" width="50%" height="50%">

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/chatbot_2.png" width="50%" height="50%">

<img src= "https://github.com/dario-t/easy_chatbot/blob/main/img/chatbot_3.png" width="50%" height="50%">


\* games.json: as the games archive with 20.000 games takes some time I have uploaded only one with 700 games

