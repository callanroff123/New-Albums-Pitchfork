################################################################################################################################################
### This module recommends a playlist (i.e., one of my own) for the top 4 popular songs of the new album #######################################
### Recommendation based on finding the playlist with the min. euclidean distance, given spotify's track metrics, with the album in question ###
### Additional option to filter out albums that aren't very similar to a playlist is used ######################################################
################################################################################################################################################ 


# Import required libraries
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime
import math
from src.config import OUTPUT_PATH, MODEL_PATH
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
import pickle


# Gets the mean track features of each of the user's (i.e., mine) playlist
def fetch_and_group_playlist_data():
    df_raw = pd.read_csv(str(OUTPUT_PATH) + "/user_playlist_tracks.csv")
    df_grouped = df_raw.groupby([
        "playlist_uri",
        "playlist_name"
    ]).agg({
        "name": "count",
        "danceability": "mean",
        "acousticness": "mean",
        "energy": "mean",
        "instrumentalness": "mean",
        "liveness": "mean",
        "loudness": "mean",
        "speechiness": "mean",
        "tempo": "mean"
    }).reset_index(drop = False).rename({
        "name": "track_count"
    })
    return(df_grouped)


# Function which stores a standard scaler model as a .pkl file
def fit_and_store_scaler(grouped_playlist_df):
    df = grouped_playlist_df.copy()
    X = df.iloc[:, 3:]
    scaler = StandardScaler()
    scaler.fit(X)
    with open(str(MODEL_PATH) + "/scaler.pkl", "wb") as file:
        pickle.dump(scaler, file)


# Gets the mean track features of the top 4 songs of each of the Pitchfork albums
# Provided they're present on Spotify
def fetch_and_preprocess_new_albums():
    df = pd.read_csv(str(OUTPUT_PATH) + "/new_album_tracks.csv").drop_duplicates(subset = ["track_uri"]).reset_index(drop = True)
    df["artist | album"] = [df["artist"][i] + " | " + df["album"][i] for i in range(len(df))]
    df_out = pd.DataFrame()
    for artist_album in df["artist | album"].unique():
        df_album = df[df["artist | album"] == artist_album].reset_index(drop = True)
        df_album["popularity_rank_in_album"] = df_album['popularity'].rank(ascending = False, method = "first")
        df_album = df_album[df_album["popularity_rank_in_album"] <= 4]
        df_out = pd.concat([df_out, df_album], axis = 0)
    df_out = df_out.reset_index(drop = True)
    df_grouped = df_out.groupby(["artist", "album"]).agg({
        "danceability": "mean",
        "acousticness": "mean",
        "energy": "mean",
        "instrumentalness": "mean",
        "liveness": "mean",
        "loudness": "mean",
        "speechiness": "mean",
        "tempo": "mean"
    }).reset_index(drop = False)
    return(df_grouped)


# Call the grouped playlist and album datasets, then transform their features using the standard scaler.
# Then get the 'closest' playlist for each album
# Option to filter out albums which are not similar to any playlist
# That is, their closest distance to a playlist still exceeds the average between-playlist distance
def album_to_playlist_recommender(remove_weird_albums = True):
    grouped_playlist_df = fetch_and_group_playlist_data()
    grouped_album_df = fetch_and_preprocess_new_albums()
    with open(str(MODEL_PATH) + "/scaler.pkl", 'rb') as file:  
        scaler = pickle.load(file)
    X_playlist_scaled = pd.DataFrame(
        scaler.transform(grouped_playlist_df.iloc[:, 3:]),
        columns = [col + "_SCALED" for col in grouped_playlist_df.iloc[:, 3:].columns]
    )
    grouped_playlist_df_scaled = grouped_playlist_df.iloc[:, 0:3].join(X_playlist_scaled)
    X_album_scaled = pd.DataFrame(
        scaler.transform(grouped_album_df.iloc[:, 2:]),
        columns = [col + "_SCALED" for col in grouped_album_df.iloc[:, 2:].columns]
    )
    grouped_album_df_scaled = grouped_album_df.iloc[:, 0:2].join(X_album_scaled)
    df_out_full = pd.DataFrame()
    for i in range(len(grouped_album_df_scaled)):
        df_alb = pd.DataFrame()
        for j in range(len(grouped_playlist_df_scaled)):
            euc_distances = euclidean_distances(
                np.array([grouped_album_df_scaled.iloc[i, 2:].values]), np.array([grouped_playlist_df_scaled.iloc[j, 3:].values])
            )[0][0]
            playlist = grouped_playlist_df_scaled.iloc[j, 1]
            artist = grouped_album_df_scaled.iloc[i, 0]
            album = grouped_album_df_scaled.iloc[i, 1]
            df_alb = pd.concat([
                df_alb,
                pd.DataFrame({
                    "artist": [artist],
                    "album": [album],
                    "recommended_playlist": [playlist],
                    "euclidean_distance": [euc_distances]
                })
            ], axis = 0).reset_index(drop = True)
        df_min_dist = df_alb[df_alb["euclidean_distance"] == min(df_alb["euclidean_distance"])]
        df_out_full = pd.concat([df_out_full, df_min_dist], axis = 0)
    df_out_full = df_out_full.reset_index(drop = True)
    if remove_weird_albums == True:
        euclid_matrx = euclidean_distances(X_playlist_scaled.values)
        euclid_values = euclid_matrx.flatten()
        mean_between_playlist_distance = np.mean([i for i in euclid_values if i != 0])
        df_out_filtered = df_out_full[df_out_full["euclidean_distance"] <= mean_between_playlist_distance].reset_index(drop = True)
        return(df_out_filtered)
    else:
        return(df_out_full)


# Runs the full similarity pipeline
def similarity_pipeline():
    grouped_playlist_df = fetch_and_group_playlist_data()
    fit_and_store_scaler(grouped_playlist_df = grouped_playlist_df)
    df_refined = album_to_playlist_recommender(remove_weird_albums = True)
    return(df_refined)

