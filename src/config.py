# Import required libraries 
import os
from pathlib import Path


# Specify path defaults
APP_PATH = Path(os.environ["PYTHONPATH"])
OUTPUT_PATH = APP_PATH / "output/"
MODEL_PATH = APP_PATH / "models/"


# Email
SMTP_SERVER = "smtp.gmail.com"
PORT = 465


# Spotify
USER = "12153998341"