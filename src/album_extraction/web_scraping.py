# 1. Load required libraries.
from pathlib import Path
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import lxml
import html
import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
from src.config import OUTPUT_PATH


# 2. Specify defaults
year = str(datetime.today().year)
options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("start-maximized")
options.add_argument("--disable-notifications")


# Gets each listing in the albums pages
def get_albums(page = "8+"):
    '''
        Gets the albums from pitchfork.com reviews

        Args:
            page (str):
                Specifies the webpage we are scraping from.
                Only accepts "main", "8+" and "best_new"

        Returns:
            DataFrame object: A dataset of all the reviewed albums on the specified webpage.
    '''
    df_final = pd.DataFrame()
    driver = webdriver.Chrome()
    if page == "main":
        url = "https://pitchfork.com/reviews/albums/"
    elif page == "8+":
        url = "https://pitchfork.com/best/high-scoring-albums/"
    elif page == "best_new":
        url = "https://pitchfork.com/reviews/best/albums/"
    else:
        raise ValueError("Only 'main', '8+' and 'best_new' allowed for page argument.")
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "lxml")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[3]/div[1]/div[2]/div/div[1]/div[1]/h1'))
    )
    reviews = soup.find_all(
        "div",
        {"class": "review"}
    )
    for review in reviews:
        artist = review.find(
            "ul",
            {"class": "review__title-artist"}
        ).find("li").text.strip()
        album = review.find(
            "h2",
            {"class": "review__title-album"}
        ).find("em").text.strip()
        genre = review.find(
            "a",
            {"class": "genre-list__link"}
        ).text.strip()
        date = review.find(
            "time",
            {"class": "pub-date"}
        ).get("datetime")
        df = pd.DataFrame({
            "Artist": [artist],
            "Album": [album],
            "Genre": [genre],
            "Date": [date]
        })
        df_final = pd.concat([df_final, df], axis = 0)
    df_final = df_final.drop_duplicates().reset_index(drop = True)
    df_final["Date"] = pd.to_datetime(df_final["Date"].str[0:10])
    driver.close()
    return(df_final)


# Main function.
# Scapes the top 24 most recent reviews.
# Then determine if they fall into the 'best new albums' category
def web_scraping_pipeline():
    df_8plus = get_albums("8+")
    df_best_albums = get_albums("best_new")
    df_best_albums["Best New Albums Flag"] = 1
    df = pd.merge(
        left = df_8plus,
        right = df_best_albums,
        on = [
            "Artist",
            "Album",
            "Genre",
            "Date"
        ],
        how = "left"
    )
    df["Best New Albums Flag"] = df["Best New Albums Flag"].fillna(0)
    df["Timestamp"] = datetime.now()
    return(df)