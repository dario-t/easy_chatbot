# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import json
import pandas as pd
from sys import platform
import os

def load_json():
    # load the archive json and return a DF
    if platform == "linux":
        dir = "game_recomendation/json/"
    else:
        dir = "game_recomendation\\json\\"
    
    if os.path.exists(dir+"games_all.json"):
        with open(dir+"games_all.json") as json_file:
            data = json.load(json_file)
        return pd.DataFrame(data)

    else:
        print("\033[1;33mFILE NO FOUND")

def data_games(df):
# -----------------------------------------------------------------------------------------------
# Take out the dates we are interested in.
# -----------------------------------------------------------------------------------------------

# List with uniques reviewer
    media_list = []
    for game in list(df.columns):
        media_list.extend(list(df[game].media.keys()))
    media_set=set(media_list)
    media_list = list(media_set)


    # dict with critics per media
    media_dict = {i:dict() for i in media_list}
    for game in df:
        for media in media_list:
            if media in df[game]["media"]:
                try: 
                    media_dict[media].update({game : float(df[game]["media"][media]["note_m"])})
                except:
                    media_dict[media].update({game : np.nan})

    # df with critics per media
    games_df = pd.DataFrame(media_dict)

    media_df = games_df.T

    return media_df, games_df


def corr_games(games_df,*games):
    # -----------------------------------------------------------------------------------------------
    # recommendation system by corelation
    # -----------------------------------------------------------------------------------------------
    df_ = games_df.corrwith(games_df.loc[games[0]], axis = 1)
    df_corr = pd.DataFrame(df_, columns = [games[0]]).dropna()
    if len(games) > 1:
        for game in games[1:]:
            df_ = games_df.corrwith(games_df.loc[game], axis = 1)
            corr_ = pd.DataFrame(df_, columns = [game]).dropna()
            df_corr = pd.concat([df_corr, corr_], axis=1, join="inner")

    df_corr["mean"] = df_corr.mean(axis=1)
    return df_corr.sort_values("mean", ascending=False)

