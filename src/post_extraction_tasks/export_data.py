# 1. Load required libraries.
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.album_extraction.web_scraping import web_scraping_pipeline
from src.spotify_tasks.etl_user_tracks import get_user_track_data
from src.spotify_tasks.etl_new_album_tracks import get_album_data
from src.config import OUTPUT_PATH, USER


# Grant access to API
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager = auth_manager)


# Export reviews to a csv file 
def export_reviews():
    '''
        Export output to CSV format
    '''
    df = web_scraping_pipeline()
    df["Date"] = pd.to_datetime(df['Date']).apply(lambda x: x.strftime("%Y-%m-%d"))
    try:
        df_hist = pd.read_csv(str(OUTPUT_PATH) + "/hist_reviews.csv")
        df_hist["Date"] = pd.to_datetime(df_hist['Date']).apply(lambda x: x.strftime("%Y-%m-%d"))
        df_hist = pd.concat([df, df_hist], axis = 0).reset_index(drop = True)
        df_hist["Timestamp"] = pd.to_datetime(df_hist["Timestamp"])
        df_hist_unique = df_hist.groupby([
            "Artist",
            "Album",
            "Genre",
            "Date"
        ]).agg("min").reset_index(drop = False)
        df_hist_unique.to_csv(str(OUTPUT_PATH) + "/hist_reviews.csv", index = False)
        df_hist_unique.to_csv(str(OUTPUT_PATH) + "/hist_reviews_backup.csv", index = False)
    except:
        df.to_csv(str(OUTPUT_PATH) + "/hist_reviews.csv", index = False)


def export_track_features(update_user_data = True):
    '''
        Export all user's playlists and review tracks to CSV format
    '''
    df_reviews = pd.read_csv(str(OUTPUT_PATH) + "/hist_reviews.csv") 
    if update_user_data == True:
        df_user_tracks = get_user_track_data(username = USER)
        df_user_tracks.to_csv(str(OUTPUT_PATH) + "/user_playlist_tracks.csv")
    else:
        pass
    try:
        df_review_full_data = pd.read_csv(str(OUTPUT_PATH) + "/new_album_tracks.csv")
        df_reviews_latest = df_reviews[df_reviews["Timestamp"] == max(df_reviews["Timestamp"])].reset_index(drop = True)
        for i in range(len(df_reviews_latest)):
            df_album_tracks = get_album_data(
                df_reviews_latest["Artist"][i], 
                df_reviews_latest["Album"][i]
            )
            df_review_full_data = pd.concat([df_review_full_data, df_album_tracks], axis = 0)
        df_review_full_data = df_review_full_data.reset_index(drop = True)
        df_review_full_data.to_csv(str(OUTPUT_PATH) + "/new_album_tracks.csv")
    except:
        df_review_full_data = pd.DataFrame()
        df_album_tracks = pd.DataFrame()
        for i in range(len(df_reviews)):
            try:
                df_album_tracks = get_album_data(
                    df_reviews["Artist"][i], 
                    df_reviews["Album"][i]
                )
            except:
                pass
            if len(df_album_tracks) > 0:
                df_review_full_data = pd.concat([df_review_full_data, df_album_tracks], axis = 0)
            else:
                pass
        df_review_full_data = df_review_full_data.reset_index(drop = True)
        df_review_full_data.to_csv(str(OUTPUT_PATH) + "/new_album_tracks.csv")