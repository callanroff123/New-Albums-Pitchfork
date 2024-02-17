# Import spotipy API
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np


# Grant access to API
auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager = auth_manager)


# Get a user's playists
def get_playlists(username):
    playlists = sp.user_playlists(username)
    playlist_uri = {}
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            p = playlist['uri']
            n = playlist["name"]
            playlist_uri[p] = n
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return(playlist_uri)


# Get the tracks within a user's playlist
def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    track_ids = []
    for i in tracks:
        track_ids.append(i['track']['id'])
    return(track_ids)
    

# Get features of a track
def get_track_features(id):
    metadata = sp.track(id)
    features = sp.audio_features(id)
    name = metadata['name']
    album = metadata['album']['name']
    artist = metadata['album']['artists'][0]['name']
    release_date = metadata['album']['release_date']
    length = metadata['duration_ms']
    popularity = metadata['popularity']
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    track = {
        "name": name,
        "album": album,
        "artist": artist,
        "release_date": release_date,
        "length": length,
        "popularity": popularity,
        "danceability": danceability,
        "acousticness": acousticness,
        "energy": energy,
        "instrumentalness": instrumentalness, 
        "liveness": liveness, 
        "loudness": loudness, 
        "speechiness": speechiness, 
        "tempo": tempo, 
        "time_signature": time_signature
    }
    return(track)


# Generate a detailed track/playlist data for a given user
def get_user_track_data(username):
    user_playlist_uris = get_playlists(username = username)
    df_out = pd.DataFrame()
    for playlist_uri in list(user_playlist_uris.keys()):
        track_uris = get_playlist_tracks(username = username, playlist_id = 'spotify:playlist:3XMV8tlCUjSsDIyGixXENN')
        for track_uri in track_uris:
            track_dict = get_track_features(track_uri)
            out_dict = {
                "playlist_uri": [playlist_uri],
                "playlist_name": [user_playlist_uris[playlist_uri]],
                "track_uri": [track_uri]
            }
            for item in track_dict.keys():
                out_dict[item] = [track_dict[item]]
            df = pd.DataFrame(out_dict)
            df_out = pd.concat([df_out, df], axis = 0)
    df_out = df_out.reset_index(drop = True)
    return(df_out)






