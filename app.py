#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import json
import websocket
import _thread as thread
import requests
from datetime import datetime, timedelta
from shapely.geometry import shape, Point

from config import REGION, USER_TOKEN, APP_TOKEN, NOTIFICATION_DELTA, MAPBOX_TOKEN

AreaBlitz = {"west": -1.58, "east": -1.03, "north": 47.17, "south": 46.84}

area = shape({ 'type': 'Polygon', 'coordinates': [REGION] })
last_strike = None

def get_city_name(lon, lat):
    mapbox_api_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places'
    url = '{}/{},{}.json?types=place&access_token={}'.format(mapbox_api_url, lon, lat, MAPBOX_TOKEN)

    response = requests.get(url)
    data = response.json()
    return data['features'][0]['text']


def on_message(ws, message):
    global last_strike
    data = json.loads(message)
    lon = data['lon']
    lat = data['lat']

    print(str(lon)+","+str(lat))

    # Strike geopoint
    point = Point(lon, lat)

    # Check if strike is inside watched area
    if area.contains(point):
        print('======== STRIKE ========')

        if last_strike:
            delta = last_strike + timedelta(minutes=NOTIFICATION_DELTA)
            now = datetime.now()
            can_notify = now > delta
        else:
            can_notify = True

        if can_notify:
            last_strike = datetime.now()

            # Display city name if Mapbox access token is set
            message = 'La foudre a frappé dans votre secteur'
            if MAPBOX_TOKEN:
                city = get_city_name(lon, lat)
                message = 'La foudre a frappé à {}.'.format(city)

            # Prepare and send Pushover notification
            params = {
                'user': USER_TOKEN,
                'token': APP_TOKEN,
                'title': 'Notiblitz',
                'message': message
            }
            requests.post('https://api.pushover.net/1/messages.json', data=params)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        time.sleep(1)
        ws.send(json.dumps(AreaBlitz))
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    port = random.randint(8050, 8090)
    ws = websocket.WebSocketApp("ws://ws.blitzortung.org:" + str(port),
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
