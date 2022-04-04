# Easy_chatbot Game recomendation
Bender ChatBot recommend videogames
________________________________________________________________________________________________________________________________________________________________________
I am currently creating this chatbot as part of a professional training. There are small bugs that need to be polished.
________________________________________________________________________________________________________________________________________________________________________

The Berder ChatBot recommends 10 games in a gui, the recommendations are taken from the Metacritic page using webScraping, the critic are taken only from the accredited media. To get the data you have to run the Meta_scraping file, which will return a .json with the info of all the games, currently there are more than 20,000 games and it takes about 14 hours to get all the info. I have uploaded a small file with a sample of the first 700 games, the rest will come later.

This project consists of 4 parts_
- Web Scraping
- Recommendation System
- Chatbot logic
- Graphical Enviroment


### Web scraping Metacritic -> meta_scraping.py
  
The scraping phase consists of 2 phases: 
- The first one takes the main page of the best games of all times and returns a list with the names of the games, the platform, the release date and the metascore and the url, and storage the dict in a json archive.

![Games of all time in Metacritic](https://github.com/dario-t/easy_chatbot/blob/main/img/Meta%20all%20games.png){width='50px'}


### Implement recommendation system: recomend_sys.py

*   Per Pearson correlation coefficient 

### ChatBoot . ->chatbot_meta.py

### Graphical Environment With TK. -> main.py

