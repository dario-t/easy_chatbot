import re
import json
from datetime import datetime
import random
import pandas as pd
import webbrowser
from recomend_sys import *
import os
from sys import platform

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if platform == "win32":
    dir = base_dir + r"json\intents.json"
else:
    dir = base_dir + "json/intents.json"

with open(dir, "r", encoding="utf-8") as j:
    json_entry = json.load(j)


# return a greeting message
def greeting():
    now = datetime.now()
    current_time = int(now.strftime("%H"))
    if current_time >= 5 and current_time < 11:
        good = "Good Morning"
    elif current_time >= 11 and current_time < 15:
        good = "Good Afternoon"
    elif current_time >= 15 and current_time < 00:
        good = "Good Evening"
    else:
        good = "Good Night"
    return good

# import df

dir_games = r"json\games.json"

with open(dir_games,"r", encoding="utf-8") as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)

def tokenizer(_input) ->list:
    # Tokenize and delete the special character
    split_message = re.split(r'\s|[,:;.?!-_]\s*', _input.lower())
    return [i for i in split_message if i != ""]

def prob(text_, list) -> float:
    # returns the probability that the input matches the sentences.
    count = 0
    for i in text_:
        if i in list: count +=1
    return count/len(text_)

def list_tok_games(games) -> list:
    return [tokenizer(i) for i in games]

def match_games(game, list_g):
    lg = list_tok_games(list_g)
    com_games = list(zip([prob(tokenizer(game),i) for i in lg], list_g, [i for i in df]))
    # TODO retrun the game in upper ans lower case
    if game in list_g:
        # if the name of the game is an exact match
        for i in com_games:
            if i[1]==game:
                return i[2]
    else:
     # return a sorted list of tuples whit his posibility
        return sorted(com_games, key = lambda tup: tup[0], reverse = True)

list_games = [i.lower() for i in df]

def search_google(input):
    # search in google
    search = input.replace(" ", "+")
    webbrowser.open(search)



def like_videogames(list_): 

    global list_fav
    list_fav = list_ # make a global variable the argument
    # conversation if like videogames
    yield random.choice(json_entry["intents"][3]["responses"]) # we ask about the game
    sent_game = yield
    g = match_games(sent_game.lower(), list_games) # we pass the match function
 
    if type(g)== str:  # if match 100% #TODO --> loop again
        list_fav.append(g) # append in fav list 
        yield random.choice(json_entry["intents"][8]["responses"]).format(g) # print the games
    else:
        list_g = ""
        choos_ = random.choice(json_entry["intents"][7]["responses"]) # ask number
        for cont, value in enumerate(g[:10]):
            list_g = "\t" + list_g + str(cont) + "-" + value[2] + "\n" # become a enumerate list
        yield random.choice(json_entry["intents"][6]["responses"]) +"\n" + list_g + "\n" + choos_
        g_entry = yield
        while True:
             # ask for the number
            try: 
                g_entry = int(g_entry)
                if g_entry >= 0 and g_entry <=9:
                    list_fav.append(g[g_entry][2]) # if become a number, append in the list
                    yield f"""{random.choice(json_entry["intents"][8]["responses"]).format(g[g_entry][2])}
{random.choice(json_entry["intents"][9]["responses"])}""" # print the games
                    
                    re_ask = yield # add another game?
                    if re_ask.lower() in json_entry["intents"][1]["patterns"]: # if not:
                        break
                    elif re_ask.lower() in json_entry["intents"][3]["patterns"]: # if add another games
                        x = like_videogames(list_fav) # start again
                        yield from x # stat again
                        break
                    else: 
                        re_ask = (random.choice(json_entry["intents"][19]["responses"])) #TODO # sorry i don´t undertand you, stat again?
                        if re_ask in json_entry["intents"][3]["patterns"]: # if yes
                             y = like_videogames(list_fav) # stat again
                             yield from y # stat again
                        elif re_ask in json_entry["intents"][1]["patterns"]: 
                            break

                else:
                    yield random.choice(json_entry["intents"][16]["responses"]) # must to be a num between 0 and 9
            except:
                if g_entry.lower() == "no": # 
                    list_g = ""
                    for cont, value in enumerate(g[10:20]):           
                        list_g = "\t" + list_g + str(cont) + "-" + value[2] + "\n" # become a enumerate list
                    yield list_g + random.choice(json_entry["intents"][13]["responses"])# in list if not say no
                    re_ask_2 = yield

                    if re_ask_2 in json_entry["intents"][1]["patterns"]: # if not
                        yield random.choice(json_entry["intents"][15]["responses"])
                        re_ask_3 = yield # sorry, do you want to add another?
                        if re_ask_3 in json_entry["intents"][1]["patterns"]: # if no
                            break
                            # yield random.choice(json_entry["intents"][10]["responses"]) # let´s go
                        elif re_ask_3 in json_entry["intents"][3]["patterns"]: # if yes
                            x = like_videogames(list_fav) # start again
                            yield from x # stat again
                            break
                    else:
                        try:
                            re_ask_2 = int(re_ask_2) # if is a number
                            if re_ask_2 >= 0 and re_ask_2 <=9:
                                list_fav.append(g[re_ask_2+10][2]) # add the game to the list
                                yield f"""{random.choice(json_entry["intents"][8]["responses"]).format(g[re_ask_2+10][2])}
{random.choice(json_entry["intents"][9]["responses"])}""" # another games?
                                re_ask =  yield
                                if re_ask.lower() in json_entry["intents"][1]["patterns"]: # if not
                                    break

                                elif re_ask.lower() in json_entry["intents"][3]["patterns"]: # if add another games
                                    x = like_videogames(list_fav) # start again
                                    yield from x # stat again
                                    break
                                
                                else:
                                    re_ask = (random.choice(json_entry["intents"][19]["responses"])) #TODO # sorry i don´t undertand you, stat again?
                                    if re_ask in json_entry["intents"][3]["patterns"]: # if yes
                                        x = like_videogames(list_fav) # start again
                                        yield from x # stat again
                                        break
                                    elif re_ask in json_entry["intents"][1]["patterns"]: 
                                        break
                                        # yield random.choice(json_entry["intents"][10]["responses"]) # let´s go
                                    break
                            else:
                                yield random.choice(json_entry["intents"][16]["responses"]) # must to be a num between 9 and 19
                                break
                                
                        except: # not a number
                            yield random.choice(json_entry["intents"][18]["responses"]) # neither number nor negation, start over.
                            break


def bot():
    # main function
    # _______________________________
    # play a sound
    # playsound("C:\\Users\\Ich\\OneDrive\\python\\Proyect\\Meta_chat_bot\\Im Bender.mp3")
    # ask if you like videogames 
    yield random.choice(json_entry["intents"][0]["responses"]).format(greeting())
    
    x = 0
    while True: 
        r = yield
        if r.lower() in json_entry["intents"][1]["patterns"]: sent_1 = 1 # if yes
        elif r.lower() in json_entry["intents"][3]["patterns"]: sent_1 = 3 # if no
        else: sent_1 = 4 # if not understand

        # don´t like videogames
        if sent_1 == 1:
            r = yield random.choice(json_entry["intents"][sent_1]["responses"])

        # looking in google
            r_1 = yield 
            yield f"Then do you like {r_1}?"
            webbrowser.open("https://www.google.com/search?q=" + r_1)
            break
            
        # Like videogames
        elif sent_1 == 3: 
            fav_games = [] 
            y = like_videogames(fav_games)
            # while True:
            yield from y
            df_ = load_json()
            media_df, games_df = data_games(df_)

            #  Recommended list of games sorted by correlation.
            a = load_json()
            media_df, games_df = data_games(a)

            y = corr_games(games_df, fav_games)
            output_str = "Ok, here is a list of games that you might like to play \n"
            output_str += f'\n\tPos,\tAffinity\t\t Game\n\t{"_"*60}'
            for i in range(10):
                output_str += f'\n\t{i}\t {round(y["mean"][i], 4)}\t\t -{y.index[i]}'
            output_str += "\n\nNow choose a game from the list for more information"
            yield output_str
            info_num = yield # choose a game from the list

            # Show info about the game
            info_num = int(info_num)
            if info_num >= 0 and info_num <= 10:
                df = load_json()
                df_game = df[y.index[info_num]] # get the game
                yield f"""Ok, here is the information about\n\n{y.index[info_num]}
Platform\t{df_game["platform"]}

Date\t{df_game["date"]}

Develop.\t{df_game["developer"]}

Geners\t{df_game["geners"]}

Rating{df_game["metascore"]}

Description\t{df_game["description"]}
                
If you want more info, just let me know"""
                finla_input = yield
                if finla_input.lower() in json_entry["intents"][3]["patterns"]:
                    webbrowser.open(df_game['url'])


                break
                
                        
        else: 
            x += 1
            if x == 2:
                yield "ok, you are very funny, Hasta la vista"
                break

