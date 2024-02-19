import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from src.spotify_tasks.etl_user_tracks import get_track_features


# Grant access to API
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager = auth_manager)


# Get tracks given an artist and album name
def get_tracks(artist_name, album_name):
    results = sp.search(
        q = f"artist:{artist_name} album:{album_name}",
        type = "album"
    )
    if results["albums"]["total"] == 0:
        return([])
    else:
        pass
    album = results["albums"]["items"][0]
    album_uri = album["id"]
    results = sp.album_tracks(album_id = album_uri)
    tracks = {}
    for track in results["items"]:
        tracks[track["id"]] = track["name"]
    return(tracks)


# Alternative to the above if no results rendered
def get_tracks_alt(artist_name, album_name):
    results = sp.search(q=f'artist:{artist_name}', type='artist', limit=1)
    if not results['artists']['items']:
        raise ValueError(f"Artist '{artist_name}' not found.")
    artist_id = results['artists']['items'][0]['id']
    results = sp.artist_albums(artist_id, album_type='album')
    album_id = None
    for album in results['items']:
        if album['name'] == album_name:
            album_id = album['id']
            break
    if not album_id:
        raise ValueError(f"Album '{album_name}' by '{artist_name}' not found.")
    results = sp.album_tracks(album_id)
    tracks = {}
    for track in results["items"]:
        tracks[track["id"]] = track["name"]
    return(tracks)


# Get features of each track and return album as a dataframe object
def get_album_data(artist_name, album_name):
    df_out = pd.DataFrame()
    album_tracks = get_tracks(artist_name = artist_name, album_name = album_name)
    if len(album_tracks) == 0:
        album_tracks = get_tracks_alt(artist_name = artist_name, album_name = album_name)
    else:
        pass
    for track_uri in album_tracks.keys():
        track_detail = get_track_features(track_uri)
        out_dict = {
                "track_uri": [track_uri]
            }
        for detail in track_detail.keys():
            out_dict[detail] = [track_detail[detail]]
        df = pd.DataFrame(out_dict)
        df_out = pd.concat([df_out, df], axis = 0)
    df_out = df_out.reset_index(drop = True)
    return(df_out)
