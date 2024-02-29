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