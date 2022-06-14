import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient

client = MongoClient("mongodb+srv://*****:********@cluster0.fdmnl.mongodb.net/?retryWrites=true&w=majority") # change ****:****** to your account and password
db = client["*******"] # change **** to a client name
collection = db["games"]

def soup_web(url_s, term=""):

    # Metacritic has an anti Web scraping script, whit user-agent we can hook the script 
    user_agent = {"User-agent": "Mozilla/5.0"}
    response  = requests.get(url_s + term, headers = user_agent)
    return BeautifulSoup(response.text, "html.parser")

def pag_scrapp():

    control_time = 1

    

    # -----------------------------------------------------------------------------
    #  add to the games, a _id  the critic score, published and gener(s)
    # -----------------------------------------------------------------------------

    # create a list of all the games in the database that not have metavalues
    # we do it to discard the games that have already scraperd the metavalues

    games_url = [(g["title"], g["url"]) for g in collection.find() if not "metavalue" in g]

    number_games = len(games_url)
    
    for game in games_url:
        time_scrap = time.time()
        control_time +=1
        url_ = game[1]
        game_name = game[0]
        soup = soup_web(url_)

        # if error return None
        def er(soup_obj, ind):
            try: return soup_obj[ind].get_text().strip()
            except: return None
              
        publisher = er(soup.find_all("a", attrs= {"class":"button"}), 0)
        geners = er(soup.find_all("span", attrs= {"class":"genre"}), 0)
        
        try:
            geners = soup.find_all(
                "li", attrs= {"class":"summary_detail product_genre"})[0].text.replace("Genre(s):","").split(",")
            geners = [i.strip() for i in geners]
        except: 
            geners = None

        metavalue = int(er(soup.find_all("span", attrs= {"itemprop":"ratingValue"}), 0))
        
        # Now we take all the critics
        url_c_ = url_ + "/critic-reviews"
        soup = soup_web(url_c_)

        list_media = [soup.find_all("div", class_="source")[i].text 
                    for i in range(len(soup.find_all("div", class_="source")))]

        score_media = [er(soup.select('div[class*="metascore_w medium game"]'),i)  
                        if isinstance(er(soup.select('div[class*="metascore_w medium game"]'),i), str) 
                        else None 
                        for i in range(len(soup.select('div[class*="metascore_w medium game"]')))]

        dict_score_media = dict(zip(list_media, score_media))

        collection.update_one({"title": game_name}, {"$set": {
                                "metavalue": metavalue, 
                                "publisher": publisher, 
                                "geners": geners, 
                                "critic_score": dict_score_media}},)

        # show the progress
        if control_time % 5 == 0:
            print(f"games remain {number_games-control_time}-- time remaining: {((number_games-control_time)/5)*(time.time()-time_scrap)/60:.2f}  min")

            

def main_scrap():
    # -----------------------------------------------------------------------------
    #  scrap the games, the platform, the release date, the metascore and the url
    #  and storage the dict in MongoDB
    # -----------------------------------------------------------------------------

# First page to open with the list of the first 100 games to scraped

    url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page="

    # last_pag-> Until which page we want to do scraping
    soup = soup_web(url,"0")
    last_pag = int(soup.find_all("a", attrs={"class":"page_num"})[-1].text) - 1

    
    for i in range(0,last_pag):

        t = time.time()

        list_games = list()
        
        # --------------------------------------------------------------------------
        # Create a dict, then scrapper the entry list web, then scraped per games, 
        # then storage the dict in a json
        # --------------------------------------------------------------------------- 
        
        soup = soup_web(url, str(i))

        # Number of titles per page
        num_title = len(soup.find_all("div", attrs = {"class":"summary"}))

        for game in range(num_title):
            title_ = soup.find_all("a", attrs = {"class":"title"})[game].text
            if title_ in (g["title"] for g in list_games):

                # If game is already included and it is not in the dict
                # Add the platform to the dict and go to the next game
                clam_details = soup.find_all("div", attrs = {"class":"clamp-details"})[game]
                platform_ = clam_details.find_all("span")[1].text[41:-77]   
                # add platform to the dict in a list
                for ga in list_games:
                    if ga["title"] == title_:
                        ga["platform"].append(platform_)

            else:

                # If the game is not in the dict    
                clam_details = soup.find_all("div", attrs = {"class":"clamp-details"})[game]
                platform_ = clam_details.find_all("span")[1].text[41:-77]
                
                # Whit "/" we create a list of 2, and we can take the 2nd element.
                url_tittle_sort = "/"+soup.find_all("a", attrs = {"class":"title"})[game]["href"] 
                url_title_ = "https://www.metacritic.com" + url_tittle_sort
                game_descr_ = soup.find_all("div", attrs = {"class":"summary"})[game].text[25:-2]
                date_ = clam_details.find_all("span")[2].text

                # Update de dictionary with the new game
                dict_game = dict()
                dict_game.update({"title": title_})
                dict_game.update({"platform": [platform_]})
                dict_game.update({"url": url_title_})
                dict_game.update({"description": game_descr_})
                dict_game.update({"date": date_})
                dict_game.update({"media": dict()})

                list_games.append(dict_game)
        
        
        collection.insert_many(list_games)

            
        print(8*"-", "PAGE", i, f"Time remaining: {(last_pag-i)*(time.time()-t)/60:.2f} min", 8*"-")

# run first time to scrap the list of the games

if __name__ == "__main__":
    main_scrap()
    pag_scrapp()
