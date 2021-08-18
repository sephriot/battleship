import asyncio
import time

from message.Message import PlayerDisconnectedMessage


class Game:
    lastActivity = time.time()
    players = []

    def __init__(self):
        self.players = []
        self.lastActivity = time.time()

    def add_player(self, websocket):
        self.players.append(websocket)

    async def handle(self, websocket, message):
        self.lastActivity = time.time()
        if len(self.players) == 2:
            await self.sendToOther(websocket, message)

    async def sendToOther(self, websocket, message):
        for player in self.players:
            if player == websocket:
                continue
            await asyncio.sleep(0.5)
            await player.send(message)

    async def timeout(self):
        for player in self.players:
            await player.send("Timeout")

    async def handleDisconnect(self, websocket):
        if self.players == 1:
            return
        await self.sendToOther(websocket, PlayerDisconnectedMessage().toJSON())
        if self.players[0] == websocket:
            del self.players[0]
        else:
            del self.players[1]
