from urllib.request import urlopen
import re
import json
from datetime import datetime
import random
from googlesearch import search
import pandas as pd

dir = "C:\\Users\\Ich\\OneDrive\\python\\Proyect\\Meta_chat_bot\\intents.json"

with open(dir, "r", encoding="utf-8") as json_file:
    json_entry = json.load(json_file)


# return a greeting message
now = datetime.now()
current_time = int(now.strftime("%H"))
if current_time >= 5 and current_time < 11:
    good = "Good Morning"
elif current_time >= 11 and current_time < 15:
    good = "Good Afternoon"
elif current_time >= 15 and current_time < 00:
    good = "Goof Evening"
else:
    good = "Good Night"

# import df

dir_games = "C:\\Users\\Ich\\OneDrive\\python\\Proyect\\Meta_chat_bot\\json\\games.json"

with open(dir_games,"r", encoding="utf-8") as json_file:
    data = json.load(json_file)
    print(data)

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


def like_videogames(list_fav):
    # conversation if like videogames
    sent_game = input(random.choice(json_entry["intents"][3]["responses"])) # we ask about the game
    g = match_games(sent_game.lower(), list_games) # we pass the match function
 
    if type(g)== str:  # if match 100%
        list_fav.append(g) # append in in fav list 
        print(random.choice(json_entry["intents"][8]["responses"]).format(g)) # print the games
    else:
        print(random.choice(json_entry["intents"][6]["responses"])) # if not match
        for cont, value in enumerate(g[:10]):
            print(cont, value[2]) # become a enumerate list
         
        while True:
            g_entry = input(random.choice(json_entry["intents"][7]["responses"])) # ask for the number
            try: 
                g_entry = int(g_entry)
                if g_entry >= 0 and g_entry <=9: 
                    list_fav.append(g[g_entry][2]) # if become a nummber, append in the list
                    print(random.choice(json_entry["intents"][8]["responses"]).format(g[g_entry][2])) # print the games
                    re_ask = input(random.choice(json_entry["intents"][9]["responses"])) # add another game?
                    if re_ask.lower() in json_entry["intents"][1]["patterns"]: # if not:
                        print(random.choice(json_entry["intents"][10]["responses"])) # let´s go
                        return list_fav
                        break
                    elif re_ask.lower() in json_entry["intents"][3]["patterns"]: # if add another games
                        like_videogames(list_fav) # stat again
                        break
                    else: 
                        re_ask = (random.choice(json_entry["intents"][19]["responses"])) #TODO # sorry i don´t undertand you, stat again?
                        if re_ask in json_entry["intents"][3]["patterns"]: # if yes
                            like_videogames(list_fav) # stat again
                            break
                        elif re_ask in json_entry["intents"][1]["patterns"]: 
                            print(random.choice(json_entry["intents"][10]["responses"])) # let´s go
                            return list_fav
                            break                         

                else:
                    print(random.choice(json_entry["intents"][16]["responses"])) # must to be a num between 0 and 9
            except:
                if g_entry.lower() == "no": # no t in list                    print(random.choice(json_entry["intents"][12]["responses"])) # show you another list
                    for cont, value in enumerate(g[10:20]):           
                        print(cont, value[2]) # print the list
                    re_ask_2 = input(random.choice(json_entry["intents"][13]["responses"]))# in list if not say no
                    if re_ask_2 in json_entry["intents"][1]["patterns"]: # if not
                        re_ask_3 = input(random.choice(json_entry["intents"][15]["responses"])) # sorry, do you want to add another?
                        if re_ask_3 in json_entry["intents"][1]["patterns"]: # if in no
                            print(random.choice(json_entry["intents"][10]["responses"])) # let´s go!
                            return list_fav
                            break
                        elif re_ask_3 in json_entry["intents"][3]["patterns"]: # if yes
                            like_videogames(list_fav) # stat again
                            break
                    else:
                        try:
                            re_ask_2 = int(re_ask_2) # if is a number
                            if re_ask_2 >= 0 and re_ask_2 <=9:
                                list_fav.append(g[re_ask_2+10][2]) # add the game to the list
                                print(random.choice(json_entry["intents"][8]["responses"]).format(g[re_ask_2+10][2])) # print the game
                                re_ask = input(random.choice(json_entry["intents"][9]["responses"])) # another games?
                                if re_ask.lower() in json_entry["intents"][1]["patterns"]: # if not
                                    print(random.choice(json_entry["intents"][10]["responses"])) # let´s go
                                    return list_fav
                                    break
                                elif re_ask.lower() in json_entry["intents"][3]["patterns"]: # if add another games
                                    like_videogames(list_fav)
                                
                                else:
                                    re_ask = (random.choice(json_entry["intents"][19]["responses"])) #TODO # sorry i don´t undertand you, stat again?
                                    if re_ask in json_entry["intents"][3]["patterns"]: # if yes
                                        like_videogames(list_fav) # stat again
                                        break
                                    elif re_ask in json_entry["intents"][1]["patterns"]: 
                                        print(random.choice(json_entry["intents"][10]["responses"])) # let´s go
                                        return list_fav
                                        break                         
                                    break
                            else:
                                print(random.choice(json_entry["intents"][16]["responses"])) # must to be a num between 9 and 19
                                break
                                
                        except: # not a number
                            print(random.choice(json_entry["intents"][18]["responses"])) # neither nummber nor negation, start over.
                            break

def bot():
    # main function
    y = yield random.choice(json_entry["intents"][0]["responses"]).format(good)
    y # ask if you like videogames 
    x = 0
    while True: 
        r = yield
        if r.lower() in json_entry["intents"][1]["patterns"]: sent_1 = 1 # si es negativo
        elif r.lower() in json_entry["intents"][3]["patterns"]: sent_1 = 3 # si es afirmativo
        else: sent_1 = 4

        # don´t like videogames
        if sent_1 == 1:
            sent_1_togoogle = input(json_entry["intents"][sent_1]["responses"])
            print(json_entry["intents"][2]["responses"][0].format(sent_1_togoogle))
            for i in search(sent_1_togoogle, stop = 1):
                print(i)
            print(json_entry["intents"][14]["responses"][0])
            break
            
        # Like videogames
        elif sent_1 == 3: 
            fav_games = [] 
            like_videogames(fav_games)
            return fav_games
            break 
        
        else: 
            x += 1
            if x == 2: 
                print("ok, you are very funny, Hasta la vista")
                break
            sent_0 = input(random.choice(json_entry["intents"][sent_1]["responses"]))
# y = bot()

