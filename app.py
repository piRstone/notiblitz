#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import json
import logging
import argparse
import websocket
import _thread as thread
import requests
from datetime import datetime, timedelta
from shapely.geometry import shape, Point

from config import REGION, USER_TOKEN, APP_TOKEN, NOTIFICATION_DELTA, MAPBOX_TOKEN

###
parser = argparse.ArgumentParser(
    description="Get notified when a lightning strikes in your area."
)
parser.add_argument("-v", "--verbose", help="Display DEBUG logs", action="store_true")

args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("notiblitz")


AreaBlitz = {"west": -1.58, "east": -1.03, "north": 47.17, "south": 46.84}

area = shape({"type": "Polygon", "coordinates": [REGION]})
last_strike = None


def get_city_name(lon, lat):
    mapbox_api_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    url = "{}/{},{}.json?types=place&access_token={}".format(
        mapbox_api_url, lon, lat, MAPBOX_TOKEN
    )

    response = requests.get(url)
    data = response.json()
    return data["features"][0]["text"]


def decode(b):
    e = {}
    d = list(b)
    c = d[0]
    f = c
    g = [c]
    h = 256
    o = h
    for b in range(1, len(d)):
        a = ord(d[b])
        a = d[b] if h > a else e.get(a, f + c)
        g.append(a)
        c = a[0]
        e[o] = f + c
        o += 1
        f = a

    return "".join(g)


def on_message(ws, message):
    global last_strike
    data = json.loads(decode(message))
    lon = data["lon"]
    lat = data["lat"]

    logger.debug(str(lon) + "," + str(lat))

    # Strike geopoint
    point = Point(lon, lat)

    # Check if strike is inside watched area
    if area.contains(point):
        logger.debug("======== STRIKE ========")

        if last_strike:
            delta = last_strike + timedelta(minutes=NOTIFICATION_DELTA)
            now = datetime.now()
            can_notify = now > delta
        else:
            can_notify = True

        if can_notify:
            last_strike = datetime.now()

            # Display city name if Mapbox access token is set
            message = "La foudre a frappé dans votre secteur"
            if MAPBOX_TOKEN:
                city = get_city_name(lon, lat)
                message = "La foudre a frappé à {}.".format(city)

            # Prepare and send Pushover notification
            send_notification(message)


def on_error(ws, error):
    logger.error(error)


def on_close(ws):
    logger.warning("### closed ###")


def on_open(ws):
    def run(*args):
        time.sleep(1)
        # ws.send(json.dumps(AreaBlitz))
        ws.send('{"a": 418}')  # Get worldwide strikes

    thread.start_new_thread(run, ())


def send_notification(message):
    params = {
        "user": USER_TOKEN,
        "token": APP_TOKEN,
        "title": "Notiblitz",
        "message": message,
    }
    requests.post("https://api.pushover.net/1/messages.json", data=params)


if __name__ == "__main__":
    websocket.enableTrace(True)

    hosts = ["ws1", "ws7", "ws8"]
    host = random.choice(hosts)
    url = f"wss://{host}.blitzortung.org:443"
    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
