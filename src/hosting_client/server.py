import socket
import json
import threading
import time

import pynput.keyboard

from logger import setupLogging
from constants import ENCODING, DISCONNECT, REQ_DATA, SHIP_TYPE, SHIPS
from _thread import start_new_thread
import logging
from pynput import keyboard

server = "127.0.0.1"
port = 80
header = 64


class SOTData:
    SHIP_CLASS: SHIP_TYPE = "SLOP"
    STEERING_PERCENT = 0  # this goes into negatives if going left and positive when going right
    SAILS_STATUS: list[float] = [100.0]

    def __init__(self, shipClass: SHIP_TYPE = "SLOP"):
        self.SHIP_CLASS = shipClass

    def jsonify(self):
        ret = "{"

        ret += f'"SHIP_CLASS": "{self.SHIP_CLASS}",'
        ret += f'"STEERING_PERCENT": {self.STEERING_PERCENT},'
        ret += f'"SAILS_STATUS": {self.SAILS_STATUS}'

        return ret + "}"

    def from_json(self, rawdata: str):
        data = json.loads(rawdata)

        self.SHIP_CLASS = data["SHIP_CLASS"]
        self.STEERING_PERCENT = data["STEERING_PERCENT"]
        self.SAILS_STATUS = data["SAILS_STATUS"]

        return self


def send(msg: str, conn: socket.socket):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    send_length = str(msg_length).encode(ENCODING)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(message)


def recv(conn) -> str:
    length = int(conn.recv(header).decode(ENCODING).replace(" ",
                                                            ''))  # if it doesn't int that means something went really wrong, so it is ok to crash

    return conn.recv(length).decode(ENCODING)


class Listen:
    def __init__(self, ship):
        self.keys = []
        self.listen = keyboard.Listener(on_press=self.on_press)
        self.data = ship

    def on_press(self, key) -> None:
        if key == keyboard.Key.delete:
            return  # stop
        try:
            k = key.char
        except:
            k = key.name  # other keys

        self.keys.append(k)

    def start(self):
        self.listen.start()

    def threaded_listen(self):
        while True:
            if '=' in self.keys:
                self.keys.remove('=')
                self.data.STEERING_PERCENT = 0
                if self.data.SHIP_CLASS == 'SLOP':
                    self.data.SAILS_STATUS = [100.0]

                elif self.data.SHIP_CLASS == 'BRIG':
                    self.data.SAILS_STATUS = [100.0, 100.0]

                elif self.data.SHIP_CLASS == 'GALL':
                    self.data.SAILS_STATUS = [100.0, 100.0, 100.0]

            elif '<101>' in self.keys:
                self.keys.remove('<101>')
                self.data.STEERING_PERCENT = 0

            elif '<102>' in self.keys:
                self.keys.remove('<102>')
                self.data.STEERING_PERCENT = 25

            print(self.keys)

            time.sleep(0.25)


def threaded_client(conn, logger, listener: Listen):
    ship: SOTData = listener.data
    send(ship.jsonify(), conn)

    while True:
        try:
            ship: SOTData = listener.data
            print(ship.STEERING_PERCENT)
            data = recv(conn)

            if data == DISCONNECT:
                logger.info("Disconnected")
                break

            elif data == REQ_DATA:
                send(ship.jsonify(), conn)

        except Exception as err:
            raise err

    logger.info("Connection Closed")
    conn.close()


def main():
    OverAllListeningLevel = logging.DEBUG
    logger = setupLogging("server-0", level=OverAllListeningLevel)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    current_ship: SHIP_TYPE = input("What is the class of the current ship (GALL, BRIG, SLOP): ")  # noqa ;there is chek

    if current_ship not in SHIPS:
        raise TypeError("Not a real ship (ALL UPPER)")

    logger.info(f"Deploying SOT ship of `{current_ship}` class.")

    SHIP = SOTData(current_ship)

    try:
        s.bind((server, port))
    except OSError:
        logger.error(f"Failed binding to {server}:{port}.")
        if OverAllListeningLevel == logging.DEBUG:
            logger.debug("DUE TO LOGGING.DEBUG:")
            logger.info("Reattempting binding to a port 1 higher!")
            s.bind((server, port + 1))

    s.listen()
    logger.info("Waiting for connection")
    li = Listen(SHIP)
    li.start()

    start_new_thread(li.threaded_listen, ())

    currentPlayer = 0
    while True:
        connection, addr = s.accept()
        logger.info(f"Connected to: {addr}")

        CL = setupLogging(f"server-{currentPlayer + 1}", level=OverAllListeningLevel)
        start_new_thread(threaded_client, (connection, CL, li))
        currentPlayer += 1


if __name__ == '__main__':
    main()
