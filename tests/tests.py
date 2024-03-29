# Import libraries/modules
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from src.config import OUTPUT_PATH
from src.sms.twilio_base import send_text_message


# New albums track features seems to be playing up.
# Can we see how it's tracking by looking at data for latest releases?
df_album_tracks = pd.read_csv(str(OUTPUT_PATH) + "/new_album_tracks.csv").sort_values("release_date", ascending = False).reset_index(drop = True)
df_album_tracks = df_album_tracks.iloc[:, 2:]
df_album_tracks[df_album_tracks["artist"] == "Brittany Howard"]


# Check if SMS functionality is working
send_text_message("Hey bishh")