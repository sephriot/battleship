import asyncio
import json
import math
import string
import time
import random

import websockets

from message.Message import BaseMessage, PlayerConnectedMessage
from backend.game import Game


class Server:
    clearInterval = 60
    games = {}  # Id, obiekt gry
    websocketToGame = {}  # websocket, ID Gry

    gameKeys = ['A', 'B', 'C']

    async def clearOldGames(self):
        while True:
            size = len(self.games)
            if size == 0:
                print("No games to clear")
                await asyncio.sleep(self.clearInterval)
                continue
            print("Starting cleanup")
            for key in self.games.copy():
                if time.time() - self.games[key].lastActivity > self.clearInterval:
                    try:
                        await self.games[key].timeout()
                    except:
                        print("Error during timeout notification")
                    print("Game deleted", key)
                    del self.games[key]
                await asyncio.sleep(self.clearInterval / size)

    async def handle(self, websocket, path):
        try:
            async for message in websocket:
                if websocket not in self.websocketToGame:
                    try:
                        m = BaseMessage(data=json.loads(message))
                        if m.type == m.PLAYER_CONNECTED:
                            self.websocketToGame[websocket] = m.gameId
                        else:
                            websocket.send("You need to connect to a game first")
                    except AttributeError:
                        websocket.send("You need to connect to a game first")
                    if self.websocketToGame[websocket] in self.games:
                        print("Adding player to game", self.websocketToGame[websocket])
                        self.games[self.websocketToGame[websocket]].add_player(websocket)
                    else:
                        if self.websocketToGame[websocket] == "":
                            self.websocketToGame[websocket] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
                            await websocket.send(PlayerConnectedMessage(self.websocketToGame[websocket]).toJSON())
                        print("Creating game", self.websocketToGame[websocket])
                        self.games[self.websocketToGame[websocket]] = Game()
                        self.games[self.websocketToGame[websocket]].add_player(websocket)

                if self.websocketToGame[websocket] in self.games:
                    game = self.games[self.websocketToGame[websocket]]
                    await game.handle(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            if self.websocketToGame[websocket] in self.games:
                game = self.games[self.websocketToGame[websocket]]
                try:
                    await game.handleDisconnect(websocket)
                except:
                    print("Trudno")
            self.websocketToGame.pop(websocket)


s = Server()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(s.handle, 'localhost', 8765)
)
asyncio.get_event_loop().run_until_complete(
    s.clearOldGames()
)

asyncio.get_event_loop().run_forever()
