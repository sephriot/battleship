import asyncio
import json
import time

import websockets

from backend.game import Game
from message.Message import BaseMessage, GameIDNowAllowedMessage


class Server:
    clearInterval = 60
    games = {}  # Id, obiekt gry
    websocketToGame = {}  # websocket, ID Gry

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
                    m = BaseMessage(data=json.loads(message))
                    try:
                        if m.type == BaseMessage.PLAYER_CONNECTED:
                            self.websocketToGame[websocket] = m.gameId
                    except AttributeError:
                        await websocket.send("I do not know what you want")

                    if self.websocketToGame[websocket] == "":
                        await websocket.send(GameIDNowAllowedMessage().toJSON())
                        self.websocketToGame.pop(websocket)
                        continue

                    if self.websocketToGame[websocket] in self.games:
                        print("Adding player to game", self.websocketToGame[websocket])
                        self.games[self.websocketToGame[websocket]].add_player(websocket)
                    else:
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
