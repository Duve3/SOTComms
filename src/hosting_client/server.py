import socket
import json
import time
from logger import setupLogging
from constants import ENCODING, DISCONNECT, REQ_DATA, SHIP_TYPE, SHIPS
from _thread import start_new_thread
import logging
from pynput import keyboard

server = ""
port = 25565
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
    def __init__(self, ship, logger):
        self.keys = []
        self.listen = keyboard.Listener(on_press=self.on_press)
        self.data = ship
        self.logger: logging.Logger = logger

    def on_press(self, key: keyboard.KeyCode) -> None:
        self.keys.append(getattr(key, 'vk', None))

    def start(self):
        self.listen.start()

    def threaded_listen(self):
        while True:
            if keyboard.KeyCode(char="=").vk in self.keys:
                self.keys.remove(keyboard.KeyCode(char="=").vk)
                self.data.STEERING_PERCENT = 0
                if self.data.SHIP_CLASS == 'SLOP':
                    self.data.SAILS_STATUS = [100.0]

                elif self.data.SHIP_CLASS == 'BRIG':
                    self.data.SAILS_STATUS = [100.0, 100.0]

                elif self.data.SHIP_CLASS == 'GALL':
                    self.data.SAILS_STATUS = [100.0, 100.0, 100.0]

            elif 101 in self.keys:
                self.keys.remove(101)
                self.data.STEERING_PERCENT = 0
                self.logger.info("Steering set to 0%")

            elif 97 in self.keys:
                self.keys.remove(97)
                self.data.STEERING_PERCENT = -25
                self.logger.info("Steering set to -25%")

            elif 100 in self.keys:
                self.keys.remove(100)
                self.data.STEERING_PERCENT = -50
                self.logger.info("Steering set to -50%")

            elif 103 in self.keys:
                self.keys.remove(103)
                self.data.STEERING_PERCENT = -75
                self.logger.info("Steering set to -75%")

            elif 104 in self.keys:
                self.keys.remove(104)
                self.data.STEERING_PERCENT = -100
                self.logger.info("Steering set to -100%")

            elif 105 in self.keys:
                self.keys.remove(105)
                self.data.STEERING_PERCENT = 25
                self.logger.info("Steering set to 25%")

            elif 102 in self.keys:
                self.keys.remove(102)
                self.data.STEERING_PERCENT = 50
                self.logger.info("Steering set to 50%")

            elif 99 in self.keys:
                self.keys.remove(99)
                self.data.STEERING_PERCENT = 75
                self.logger.info("Steering set to 75%")

            elif 98 in self.keys:
                self.keys.remove(98)
                self.data.STEERING_PERCENT = 100
                self.logger.info("Steering set to 100%")

            time.sleep(0.25)


def threaded_client(conn, logger, listener: Listen):
    ship: SOTData = listener.data
    send(ship.jsonify(), conn)

    while True:
        try:
            ship: SOTData = listener.data
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

    LL = setupLogging("key-listen", level=OverAllListeningLevel)
    li = Listen(SHIP, LL)
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
