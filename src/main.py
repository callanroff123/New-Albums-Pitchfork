###################################
### Runs the end-to-end project ###
###################################


# Allow relative importst        
import os
import sys
ENV = os.environ.get("VIRTUAL_ENV")
ENV_SPLIT = ENV.split("/")
PYTHONPATH = "/".join(i for i in ENV_SPLIT if i != "venv")
os.environ["PYTHONPATH"] = PYTHONPATH
sys.path.append(PYTHONPATH)


# Import libraries/modules
from src.post_extraction.export_data import export_reviews, export_track_features
from src.similarity_grouping.euclidean_distance import similarity_pipeline, fetch_and_group_playlist_data, fit_and_store_scaler
from src.sms.twilio_base import send_text_message
from src.config import OUTPUT_PATH
import pandas as pd


# Main function
def run_end_to_end_pipeline():
    export_reviews()
    export_track_features(update_user_data = False)
    df = fetch_and_group_playlist_data()
    fit_and_store_scaler(df)
    _df_out = similarity_pipeline(remove_weird_albums = True)
    df_reviews = pd.read_csv(str(OUTPUT_PATH) + "/hist_reviews.csv")
    df_out_final = pd.merge(
        left = df_reviews,
        right = _df_out,
        left_on = ["Artist", "Album"],
        right_on = ["artist", "album"],
        how = "inner"
    )
    df_out_final = df_out_final.drop([
        "artist",
        "album",
        "euclidean_distance"
    ], axis = 1).rename(columns = {
        "recommended_playlist": "Recommended Playlist"
    })
    return(df_out_final)


# Front-end program
def frontend_pipeline(send_sms = True):
    df = run_end_to_end_pipeline()
    df_new_albums = df[df["Timestamp"] == max(df["Timestamp"])].reset_index(drop = True)
    if len(df_new_albums) > 0:
        msgg = "Hey there! Here's some new albums you might like to check out...\n--------------------\n"
        for i in range(len(df_new_albums)):
            artist = f"Artist: {df_new_albums['Artist'][i]}\n"
            album = f"Album: {df_new_albums['Album'][i]}\n"
            genre = f"Genre: {df_new_albums['Genre'][i]}\n"
            release = f"Release Date: {df_new_albums['Date'][i]}\n"
            playlist = f"Best Spotify User's Playlist for Songs on this Album: {df_new_albums['Recommended Playlist'][i]}\n"
            eight_plus = f"8+ Album: {df_new_albums["8+ Album Flag"][i]}\n"
            best_new = f"Best New Album: {df_new_albums["Best New Albums Flag"][i]}\n" 
            lines = "--------------------\n"
            msgg = msgg + lines + artist + album + genre + release + playlist + eight_plus + best_new + lines
        print(msgg)
        if send_sms == True:
            send_text_message(msgg)
        else:
            pass
    else:
        print("No New Albums Unforrrrrch :/")