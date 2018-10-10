# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

SONGKICK = 'https://api.songkick.com/api/3.0/search/locations.json?query=chicago&apikey={}}'
GET_CONCERTS = 'https://api.songkick.com/api/3.0/metro_areas/{}/calendar.json?apikey={}'


def index(request):
    context = {}

    res = requests.get(SONGKICK.format('Chicago', settings.SONGKICK_API_KEY))
    metro_content = json.loads(res.content)
    metro_id = metro_content['resultsPage']['results']['location'][0]['metroArea']['id']

    concerts_res = requests.get(GET_CONCERTS.format(metro_id, settings.SONGKICK_API_KEY))
    concert_content = json.loads(concerts_res.content)
    context['concerts'] = concert_content['resultsPage']['results']['event'][0:10]

    return render(request, "concert_code/index.html", context)


