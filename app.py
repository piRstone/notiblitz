#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import time
import json
import websocket
import _thread as thread

AreaBlitz = {"west": -1.58, "east": -1.03, "north": 47.17, "south": 46.84}


def on_message(ws, message):
    data = json.loads(message)
    print(data['time'])
    print(str(data['lat'])+","+str(data['lon']))


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
