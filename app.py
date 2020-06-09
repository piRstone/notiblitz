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

from config import REGION, USER_TOKEN, APP_TOKEN, NOTIFICATION_DELTA

AreaBlitz = {"west": -1.58, "east": -1.03, "north": 47.17, "south": 46.84}

zone = shape({ 'type': 'Polygon', 'coordinates': [REGION] })
last_strike = None

def on_message(ws, message):
    global last_strike
    data = json.loads(message)
    print(str(data['lat'])+","+str(data['lon']))

    point = Point(data['lon'], data['lat'])

    if zone.contains(point):
        print('======== STRIKE ========')

        if last_strike:
            delta = last_strike + timedelta(minutes=NOTIFICATION_DELTA)
            now = datetime.now()
            can_notify = now > delta
        else:
            can_notify = True

        if can_notify:
            last_strike = datetime.now()
            params = {
                'user': USER_TOKEN,
                'token': APP_TOKEN,
                'title': 'Notiblitz',
                'message': 'La foudre a frappé dans votre secteur'
            }
            r = requests.post('https://api.pushover.net/1/messages.json', data=params)


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
