# Easy_chatbot Game recomendation
Bender ChatBot recommend videogames
________________________________________________________________________________________________________________________________________________________________________
I am currently creating this chatbot as part of a professional training. There are small bugs that need to be polished.
________________________________________________________________________________________________________________________________________________________________________

The Berder ChatBot recommends 10 games in a gui, the recommendations are taken from the Metacritic page using webScraping, the critic are taken only from the accredited media. To get the data you have to run the Meta_scraping file, which will return a .json with the info of all the games, currently there are more than 20,000 games and it takes about 14 hours to get all the info. I have uploaded a small file with a sample of the first 700 games, the rest will come later.



### Web scraping Metacritic -> Meta_scraping.py
  
*   Export dict to json archive ans safe it. 
*   from json to DataFrame. 

### Implement recommendation system: recomend_sys.py

*   Per Pearson correlation coefficient 

### ChatBoot . ->chatbot_meta.py

### Graphical environment with TK. -> main.py

