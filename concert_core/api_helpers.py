from django.conf import settings
from django.utils.http import urlquote

from concert_core.models import AccessToken

import requests
import json


SONGKICK_URL = 'https://api.songkick.com/api/3.0{}'
SONGKICK_GET_METRO_ID = '/search/locations.json?query={}&apikey=' + settings.SONGKICK_API_KEY
SONGKICK_GET_CONCERTS = '/metro_areas/{}/calendar.json?apikey=' + settings.SONGKICK_API_KEY


def songkick_rest_call(path, query_value):
    """General function for Songkick GET requests"""
    full_path = path.format(query_value)
    url = SONGKICK_URL.format(full_path)
    response = requests.get(url)
    return json.loads(response.content)


def spotify_get(path):
    """General function for Spotify GET requests"""
    access_token = AccessToken.objects.order_by('-pk')[0]
    response = requests.get(
        settings.SPOTIFY_BASE_URL + path,
        headers={'Authorization': 'Bearer {}'.format(access_token.token_value)},
    )
    return json.loads(response.content)


def spotify_post(path, data):
    """General function for Spotify POST requests"""
    access_token = AccessToken.objects.order_by('-pk')[0]
    response = requests.post(
        settings.SPOTIFY_BASE_URL + path,
        headers={'Authorization': 'Bearer {}'.format(access_token.token_value)},
        data=json.dumps(data)
    )
    return json.loads(response.content)


def get_artist_id(artist):
    """Given an artist name, get artist id from Spotify"""
    path = "/v1/search?q={}&type=artist&limit=1".format(urlquote(artist))
    artists = spotify_get(path)
    if artists['artists']['items']: #If we get artist query
        artist_id = artists['artists']['items'][0]['id']
        return artist_id


def get_artist_top_songs(artist):
    """Given an artist, get their top two songs"""
    artist_id = get_artist_id(artist)
    if artist_id:
        top_tracks_content = '/v1/artists/{}/top-tracks?country=US'.format(artist_id)
        artist_info = spotify_get(top_tracks_content)
        return [track['uri'] for track in artist_info['tracks'][:2]]


def create_playlist_spotify():
    """Create Spotify playlist"""
    path = '/v1/users/{}/playlists'.format(settings.SPOTIFY_USER_ID)
    return spotify_post(path, {'name' : 'Playlist'})


def add_songs_to_playlist(playlist_id, uris):
    """Given a playlist and a set of song uris, create a playlist"""
    path = '/v1/users/{}/playlists/{}/tracks'.format(settings.SPOTIFY_USER_ID, playlist_id)
    return spotify_post(path, {'uris': uris})


def get_new_access_token():
    """Get access token using refresh token"""
    res = requests.post('https://accounts.spotify.com/api/token', data={
        "grant_type": "refresh_token",
        "refresh_token": settings.REFRESH_TOKEN,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET
    })

    AccessToken.objects.create(token_value=json.loads(res.content)['access_token'])
