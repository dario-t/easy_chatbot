import requests
from bs4 import BeautifulSoup
import os
import json
from sys import platform


def soup_web(url_s):
    user_agent = {"User-agent": "Mozilla/5.0"}
    response  = requests.get(url_s, headers = user_agent)
    return BeautifulSoup(response.text, "html.parser")




def storage_(pag, to_stor):  
    # --------------------------------------------------------------------------
    # Storage the dict in a json archive
    # --------------------------------------------------------------------------
    
    if platform == "linux":
        dir = "/json/"
    else:
        dir = "\\json\\"

    try: 
        os.mkdir(dir)
    except FileExistsError:
        pass

    with open(dir+f"games_pag_{pag}.json", "w") as f:
        json.dump(to_stor, f)




def pag_scrapp(dict_games):

    # -----------------------------------------------------------------------------
    # take out the url per games in dict_games to scraped the critic
    # reviews, date, note and url of the reviewers
    # -----------------------------------------------------------------------------

    # firs we take the published and the gener(s):
    for game in dict_games:
        print(game)

        
        url_g_ = dict_games[game]["url"]
        soup_g = soup_web(url_g_)
        try: 
            dict_games[game]["developer"] = soup_g.find_all("a", attrs= {"class":"button"})[0].text
        except: 
            dict_games[game]["developer"] = ""
        
        try:
            geners = soup_g.find_all(
                "li", attrs= {"class":"summary_detail product_genre"})[0].text.replace("Genre(s):","").split(",")
            dict_games[game]["geners"] = [i.strip() for i in geners]
        except: 
            dict_games[game]["geners"] = ""
        
        try:
            metavalue = int(soup_g.find_all("span", attrs = {"itemprop":"ratingValue"})[0].text)
            dict_games[game]["metascore"] = metavalue
        except: dict_games[game]["metascore"] = ""

        # Now we take all the critics
        url_c_ = url_g_ + "/critic-reviews"
        soup = soup_web(url_c_)

        for i in range(len(soup.find_all("div", class_="source"))):

            reviewer = soup.find_all("div", class_="source")[i].text

            dict_games[game]["media"][reviewer] = {
                "review": soup.find_all("div", class_="review_body")[i].text.strip()}

            try : 
                dict_games[game]["media"][reviewer].update({
                "url_m": soup.find_all("a", class_="external")[i*2]["href"]})
            except: 
                dict_games[game]["media"][reviewer].update({"url_m": ""})

            try : 
                dict_games[game]["media"][reviewer].update( {
                "date_m": soup.find_all("div", class_="date")[i].text})
            except: 
                dict_games[game]["media"][reviewer].update({"date_m": ""})

            try : 
                dict_games[game]["media"][reviewer].update( {
                "note_m": soup.find_all("div", class_="review_grade")[i].strip()})
            except: 
                dict_games[game]["media"][reviewer].update({"note_m": ""})

def main_scrap():

# First page to open with the list of the first 100 games to scraped

    first_pag = str(0) 
    url = "https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page="

    # Metacritic has an anti Web scraping script, whit user-agent we can hook the script 
    user_agent = {"User-agent": "Mozilla/5.0"}

    # last_pag-> Until which page we want to do scraping
    response  = requests.get(url + "0", headers = user_agent)
    soup = BeautifulSoup(response.text, "html.parser")
    last_pag = int(soup.find_all("a", attrs={"class":"page_num"})[-1].text) - 1

    #  first_pag -> from which page we want to do scraping
    
    first_pag = str(0)

    for i in range(0,last_pag):

        # --------------------------------------------------------------------------
        # Create a dict, then scrapper the entry list web, then scraped per games, 
        # then storage the dict in a json
        # --------------------------------------------------------------------------- 
        dict_games =dict()
        
        url_ = url + str(i)
        response  = requests.get(url + str(i), headers = user_agent)
        soup = BeautifulSoup(response.text, "html.parser")

        # Number of titles per page
        num_title = len(soup.find_all("div", attrs = {"class":"summary"}))

        for game in range(num_title):
            title_ = soup.find_all("a", attrs = {"class":"title"})[game].text
            if title_ in dict_games.keys():

                # If game is already included and it is not in the dict
                # Add the platform to the dict and go to the next game
                clam_details = soup.find_all("div", attrs = {"class":"clamp-details"})[game]
                platform_ = clam_details.find_all("span")[1].text[41:-77]        
                dict_games[title_]["platform"].append(platform_)
            else:

                # If the game is not in the dict    
                clam_details = soup.find_all("div", attrs = {"class":"clamp-details"})[game]
                platform_ = clam_details.find_all("span")[1].text[41:-77]
                
                # Whit "/" we create a list of 2, and we can take the 2nd element.
                url_tittle_sort = "/"+soup.find_all("a", attrs = {"class":"title"})[game]["href"] 
                url_title_ = "https://www.metacritic.com" + url_tittle_sort
                game_descr_ = soup.find_all("div", attrs = {"class":"summary"})[game].text[25:-2]
                ranking_ = soup.find_all("a", attrs = {"class":"metascore_anchor"})[game].text[1:-1]
                date_ = clam_details.find_all("span")[2].text

                # Update de dictionary with the new game
                dict_games[title_] = {"platform": [platform_],
                                    "url":  url_title_,
                                    "description" : game_descr_, 
                                    "date" : date_,
                                    "media": dict()
                                    }
        pag_scrapp(dict_games)
        storage_(i, dict_games)
        print(8*"-", "PAGE", i, 8*"-")

main_scrap()