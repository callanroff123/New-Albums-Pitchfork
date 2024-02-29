###################################
### Runs the end-to-end project ###
###################################


# Import libraries/modules
from src.post_extraction_tasks.export_data import export_reviews, export_track_features
from src.similarity_grouping.euclidean_distance import similarity_pipeline, fetch_and_group_playlist_data, fit_and_store_scaler
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
def frontend_pipeline():
    df = run_end_to_end_pipeline()
    df_new_albums = df[df["Timestamp"] == max(df["Timestamp"])].reset_index(drop = True)
    if len(df_new_albums) > 0:
        print("Hey there! Here's some new albums you might like to check out...")
        for i in range(len(df_new_albums)):
            print("Artist: ", df_new_albums["Artist"][i])
            print("Album: ", df_new_albums["Album"][i])
            print("Genre: ", df_new_albums["Genre"][i])
            print("Release Date: ", df_new_albums["Date"][i])
            print("Best Playlist for Songs on this Album: ", df_new_albums["Recommended Playlist"][i])
    else:
        print("No New Albums Unforrrrrch :/")