import socket
import json
from constants import DISCONNECT, SHIP_TYPE, ENCODING, REQ_DATA


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

        return ret + "\b}"

    def from_json(self, rawdata: str):
        data = json.loads(rawdata)

        self.SHIP_CLASS = data["SHIP_CLASS"]
        self.STEERING_PERCENT = data["STEERING_PERCENT"]
        self.SAILS_STATUS = data["SAILS_STATUS"]

        return self


class Client:
    def __init__(self, serverIP: str):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = serverIP
        self.port = 80
        self.addr = (self.server, self.port)
        self.header = 64
        self.socket.settimeout(10)

        self.SOT: SOTData = self.connect()

    def connect(self):
        self.socket.connect(self.addr)
        data = self.recv()

        return SOTData().from_json(data)

    def refresh(self):
        self.send(REQ_DATA)
        data = self.recv()

        self.SOT = SOTData().from_json(data)

    def disconnect(self):
        self.send(DISCONNECT)

    def send(self, msg: str):
        message = msg.encode(ENCODING)
        msg_length = len(message)
        send_length = str(msg_length).encode(ENCODING)
        send_length += b' ' * (self.header - len(send_length))
        self.socket.send(send_length)
        self.socket.send(message)

    def recv(self) -> str:
        length = int(self.socket.recv(self.header).decode(
            ENCODING))  # if it doesn't int that means something went really wrong so its ok to crash
        return self.socket.recv(length).decode(ENCODING)
