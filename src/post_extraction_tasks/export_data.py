# 1. Load required libraries.
import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime
from src.album_extraction.web_scraping import web_scraping_pipeline
from src.config import OUTPUT_PATH


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