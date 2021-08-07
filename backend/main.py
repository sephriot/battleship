import asyncio
import math

import websockets

from backend.game import Game


class Server:
    clients = {}
    games = {}  # Id, obiekt gry
    websocketToGame = {}  # websocket, ID Gry

    gameKeys = ['A', 'B', 'C']

    def __init__(self):
        self.clients = {}

    async def echo(self, websocket, path):
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

                game = self.games[self.websocketToGame[websocket]]
                if len(game.players) == 2:
                    await game.handle(websocket, message)

        except RuntimeError:
            print("Error")


s = Server()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(s.echo, 'localhost', 8765)
)
asyncio.get_event_loop().run_forever()
