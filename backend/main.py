import asyncio
import math
import time

import websockets

from backend.game import Game


class Server:
    clearInterval = 5
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
                    self.websocketToGame[websocket] = self.gameKeys[math.floor(len(self.websocketToGame) / 2)]
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
