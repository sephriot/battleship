import json


class BaseMessage:
    NULL = "NULL"
    PLAYER_DISCONNECTED = "PLAYER_DISCONNECTED"
    PLAYER_CONNECTED = "PLAYER_CONNECTED"
    ATTACK = "ATTACK"
    HIT = "HIT"
    MISS = "MISS"
    SANK = "SANK"

    def __init__(self, data=None):
        self.type = self.NULL
        if data is not None:
            self.__dict__ = data

    def __init_subclass__(cls, **kwargs):
        BaseMessage.__init__(cls)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class PlayerDisconnectedMessage(BaseMessage):
    def __init__(self):
        self.type = self.PLAYER_DISCONNECTED


class PlayerConnectedMessage(BaseMessage):
    def __init__(self):
        self.type = self.PLAYER_CONNECTED


class AttackMessage(BaseMessage):
    def __init__(self, x=0, y=0):
        self.type = self.ATTACK
        self.x = x
        self.y = y


class HitMessage(BaseMessage):
    def __init__(self):
        self.type = self.HIT


class MissMessage(BaseMessage):
    def __init__(self):
        self.type = self.MISS


class SankMessage(BaseMessage):
    def __init__(self):
        self.type = self.SANK
