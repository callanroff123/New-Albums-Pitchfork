###################################
### Runs the end-to-end project ###
###################################


# Import libraries/modules
from src.post_extraction_tasks.export_data import export_reviews, export_track_features
from src.similarity_grouping.euclidean_distance import similarity_pipeline, fetch_and_group_playlist_data, fit_and_store_scaler


# Main function
def run_end_to_end_pipeline():
    export_reviews()
    export_track_features(update_user_data = False)
    df = fetch_and_group_playlist_data()
    fit_and_store_scaler(df)
    df_final = similarity_pipeline(remove_weird_albums = True)
    return(df_final)