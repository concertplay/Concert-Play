# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from concert_core.api_helpers import (songkick_rest_call, SONGKICK_GET_METRO_ID, SONGKICK_GET_CONCERTS,
                                      get_artist_top_songs, create_playlist_spotify, add_songs_to_playlist,
                                      get_new_access_token)



def index(request):
    """Home page"""
    return render(request, 'concert_core/base.html')


def get_concerts(request):
    """Get a list of concerts for a user's city search query"""
    city = request.GET.get('city', None)

    if city:
        metro_content = songkick_rest_call(SONGKICK_GET_METRO_ID, city)
        results = metro_content['resultsPage']['results']
        if not results:
            return JsonResponse({'error': 'City Not Found'}, status=404)

        metro_id = metro_content['resultsPage']['results']['location'][0]['metroArea']['id']
        concert_content = songkick_rest_call(SONGKICK_GET_CONCERTS, metro_id)
        concerts = concert_content['resultsPage']['results']['event'][-10:] # Grab only ten concerts

        return JsonResponse({'concerts': concerts}, status=200)


def create_playlist(request):
    """Create a Spotify playlist given a list of artists"""
    try:
        artists = request.POST.getlist('artists[]')
        uris = []

        for artist in artists:
            artist_song_uris = get_artist_top_songs(artist)
            if artist_song_uris:
                uris += artist_song_uris

        playlist_id = create_playlist_spotify()['id']
        add_songs_to_playlist(playlist_id, uris)

        return JsonResponse({'user_id': settings.SPOTIFY_USER_ID, 'playlist_id': playlist_id}, status=200)
    except (KeyError, IndexError) as e: # If refresh token key error or if you dont have a starting access token
        get_new_access_token()
        return render(request, 'concert_core/base.html', {})



