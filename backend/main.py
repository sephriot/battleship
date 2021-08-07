import asyncio
import math

import websockets

from backend.game import Game


class Server:
    games = {}  # Id, obiekt gry
    websocketToGame = {}  # websocket, ID Gry

    gameKeys = ['A', 'B', 'C']

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
                await game.handle(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            game = self.games[self.websocketToGame[websocket]]
            try:
                await game.handleDisconnect(websocket)
            except:
                print("Trudno")
            self.websocketToGame.pop(websocket)


s = Server()
asyncio.get_event_loop().run_until_complete(
    websockets.serve(s.echo, 'localhost', 8765)
)
asyncio.get_event_loop().run_forever()
