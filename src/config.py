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


# Phone numbers for SMS alerts
TWILIO_PHONE_NUMBER = '+19167643456'
RECIPIENT_PHONE_NUMBER = '+61481132823'
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')